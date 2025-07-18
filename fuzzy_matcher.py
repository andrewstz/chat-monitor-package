import re
from typing import List, Tuple, Optional

class FuzzyMatcher:
    """智能模糊匹配器，支持字符顺序匹配和OCR结果清理"""
    
    def __init__(self, target_contacts: List[str], similarity_threshold: float = 0.5, min_length: int = 2):
        # 清理每个目标联系人中的空格
        self.target_contacts = [self.clean_ocr_text(contact) for contact in target_contacts]
        self.similarity_threshold = similarity_threshold
        self.min_length = min_length
    
    def clean_ocr_text(self, text: str) -> str:
        """
        清理OCR识别结果中的额外字符
        移除常见的OCR错误字符和格式
        """
        if not text:
            return ""
        
        # 移除常见的OCR错误字符
        cleaned = text
        
        # 移除开头的特殊字符组合
        cleaned = re.sub(r'^[\'\"\|\s]+', '', cleaned)
        
        # 移除结尾的特殊字符组合
        cleaned = re.sub(r'[\'\"\|\s]+$', '', cleaned)
        
        # 移除多余的空格
        cleaned = re.sub(r'\s+', '', cleaned)
        
        # 移除常见的OCR错误字符
        ocr_noise_chars = ['|', '`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '=', '{', '}', '[', ']', '\\', ':', ';', '"', "'", '<', '>', ',', '.', '?', '/']
        for char in ocr_noise_chars:
            cleaned = cleaned.replace(char, '')
        
        # 移除数字（如果目标文本不包含数字）
        # 这里可以根据需要调整
        # cleaned = re.sub(r'\d+', '', cleaned)
        
        return cleaned.strip()
    
    def calculate_edit_distance_similarity(self, recognized_text: str, target_text: str) -> float:
        """
        使用编辑距离计算相似度
        考虑字符的插入、删除、替换操作
        """
        if not recognized_text or not target_text:
            return 0.0
        
        # 清理OCR文本
        cleaned_recognized = self.clean_ocr_text(recognized_text)
        if not cleaned_recognized:
            return 0.0
        
        # 计算编辑距离
        m, n = len(cleaned_recognized), len(target_text)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        # 初始化第一行和第一列
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        
        # 填充DP表
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if cleaned_recognized[i-1] == target_text[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
        
        # 计算相似度：1 - 编辑距离/最大长度
        max_len = max(m, n)
        similarity = 1.0 - (dp[m][n] / max_len) if max_len > 0 else 1.0
        return similarity
    
    def calculate_longest_common_subsequence_similarity(self, recognized_text: str, target_text: str) -> float:
        """
        使用最长公共子序列计算相似度
        考虑字符的顺序匹配
        """
        if not recognized_text or not target_text:
            return 0.0
        
        # 清理OCR文本
        cleaned_recognized = self.clean_ocr_text(recognized_text)
        if not cleaned_recognized:
            return 0.0
        
        # 计算最长公共子序列长度
        m, n = len(cleaned_recognized), len(target_text)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if cleaned_recognized[i-1] == target_text[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        # 计算相似度：LCS长度 / 目标字符串长度
        lcs_length = dp[m][n]
        similarity = lcs_length / n if n > 0 else 0.0
        return similarity
    
    def calculate_ordered_char_similarity(self, recognized_text: str, target_text: str) -> float:
        """
        计算字符顺序子序列相似度
        识别到的字符必须在目标字符串中按顺序依次出现（中间可有其他字符），顺序不能乱。
        Returns:
            相似度 (0.0-1.0)
        """
        if not recognized_text or not target_text:
            return 0.0
        
        # 清理OCR文本
        cleaned_recognized = self.clean_ocr_text(recognized_text)
        if not cleaned_recognized:
            return 0.0
        
        target_chars = list(target_text)
        recognized_chars = list(cleaned_recognized)
        
        match_count = 0
        target_idx = 0
        # me: 核心，每个ocr的字符都拿来在原始字符串里搜索，找到就用match_count统计匹配量，没有匹配则target_idx游标继续让target_chars往前移动一个字符
        for char in recognized_chars:
            while target_idx < len(target_chars):
                if char == target_chars[target_idx]:
                    match_count += 1
                    target_idx += 1
                    break
                target_idx += 1
        
        similarity = match_count / len(target_chars) if len(target_chars) > 0 else 0.0
        return similarity
    
    def calculate_flexible_similarity(self, recognized_text: str, target_text: str) -> float:
        """
        针对OCR场景优化的相似度计算
        OCR特点：可能多出少量意外字符，可能缺少某些字符，但字符顺序不会颠倒
        """
        if not recognized_text or not target_text:
            return 0.0
        
        # 清理OCR文本
        cleaned_recognized = self.clean_ocr_text(recognized_text)
        if not cleaned_recognized:
            return 0.0
        
        target_chars = list(target_text)
        recognized_chars = list(cleaned_recognized)
        
        # 计算字符存在性匹配 这是一个生成器表达式配合sum()函数：for char in recognized_chars: 遍历OCR识别到的每个字符； 
        # if char in target_chars: 条件判断，检查字符是否在目标字符串中
        # 1: 如果条件为真，返回1（计数）
        # sum(): 将所有1相加，得到总数
        # 功能： 统计OCR识别结果中有多少个字符存在于目标字符串中，不考虑顺序。
        # 1. 字符存在性匹配 (30%)
        # 统计OCR中存在的目标字符数量
        existing_chars = sum(1 for char in recognized_chars if char in target_chars)
        # 存在性评分计算 existing_chars / len(target_chars): 条件为真时的计算
        # 0.0: 条件为假时的默认值
        # 功能说明
        # 计算字符存在性匹配率：
        # 分子：OCR中存在的字符数
        # 分母：目标字符串的总字符数
        # 结果：存在性匹配的百分比
        existence_score = existing_chars / len(target_chars) if len(target_chars) > 0 else 0.0
        
        # 2. 最长公共子序列相似度 (60%) - 主要算法
        # 处理字符缺失和额外字符问题，保持顺序
        lcs_score = self.calculate_longest_common_subsequence_similarity(cleaned_recognized, target_text)
        
        # 3. 编辑距离相似度 (10%) - 微调
        # 处理小幅度差异
        edit_distance_score = self.calculate_edit_distance_similarity(cleaned_recognized, target_text)
        
        # 针对OCR场景的权重分配
        final_score = (
            existence_score * 0.3 +      # 字符存在性
            lcs_score * 0.6 +            # 最长公共子序列 (主要)
            edit_distance_score * 0.1    # 编辑距离 (微调)
        )
        
        return final_score
    
    def match_sender(self, first_line: str) -> Optional[Tuple[str, str, float]]:
        """
        匹配发信人
        
        Args:
            first_line: 第一行文本
            
        Returns:
            Tuple[匹配到的目标联系人, 实际识别的发信人, 相似度] 或 None
        """
        if not first_line:
            return None
        
        # 清理OCR文本
        cleaned_first_line = self.clean_ocr_text(first_line)
        if len(cleaned_first_line) < self.min_length:
            return None
        
        best_match = None
        best_similarity = 0.0
        
        # 对每个目标联系人进行匹配
        for target in self.target_contacts:
            # 使用灵活的相似度计算
            similarity = self.calculate_flexible_similarity(cleaned_first_line, target)
            
            if similarity > best_similarity and similarity >= self.similarity_threshold:
                best_similarity = similarity
                best_match = target
        
        if best_match:
            return (best_match, cleaned_first_line, best_similarity)
        
        return None
    
    def debug_match_process(self, recognized_text: str, target_text: str) -> None:
        print(f"\n=== 调试匹配过程 ===")
        print(f"原始识别文本: '{recognized_text}'")
        cleaned_text = self.clean_ocr_text(recognized_text)
        print(f"清理后文本: '{cleaned_text}'")
        print(f"目标文本: '{target_text}'")
        
        target_chars = list(target_text)
        recognized_chars = list(cleaned_text)
        print(f"目标字符: {target_chars}")
        print(f"识别字符: {recognized_chars}")
        
        # 计算字符存在性匹配
        target_char_set = set(target_chars)
        existing_chars = [char for char in recognized_chars if char in target_char_set]
        existence_score = len(existing_chars) / len(target_chars) if len(target_chars) > 0 else 0.0
        print(f"字符存在性匹配: {existing_chars} ({existence_score:.2f})")
        
        # 计算顺序匹配
        target_idx = 0
        match_count = 0
        match_details = []
        
        for char in recognized_chars:
            found = False
            while target_idx < len(target_chars):
                if char == target_chars[target_idx]:
                    match_details.append(f"字符'{char}'在目标位置{target_idx}匹配")
                    match_count += 1
                    target_idx += 1
                    found = True
                    break
                target_idx += 1
            if not found:
                match_details.append(f"字符'{char}'未找到匹配")
        
        print("顺序匹配详情:")
        for detail in match_details:
            print(f"  {detail}")
        
        order_score = match_count / len(target_chars) if len(target_chars) > 0 else 0.0
        print(f"顺序匹配字符数: {match_count}/{len(target_chars)}")
        print(f"顺序匹配分数: {order_score:.2f}")
        
        # 计算编辑距离相似度
        edit_distance_score = self.calculate_edit_distance_similarity(recognized_text, target_text)
        print(f"编辑距离相似度: {edit_distance_score:.2f}")
        
        # 计算最长公共子序列相似度
        lcs_score = self.calculate_longest_common_subsequence_similarity(recognized_text, target_text)
        print(f"最长公共子序列相似度: {lcs_score:.2f}")
        
        # 综合评分
        final_score = (
            existence_score * 0.2 + 
            order_score * 0.3 + 
            edit_distance_score * 0.3 + 
            lcs_score * 0.2
        )
        print(f"综合相似度: {final_score:.2f}")
        
        return final_score

def test_fuzzy_matcher():
    """测试智能模糊匹配功能"""
    # 测试配置
    target_contacts = ["【常规】 客户端项目", "js_wbmalia-研发部助理"]
    matcher = FuzzyMatcher(target_contacts, similarity_threshold=0.5, min_length=2)
    
    # 测试用例（包含OCR错误的情况）
    test_cases = [
        "j          【常规】 客户端项目                               |", "【常规】 客户端项目",
        "'|          【常规】 客户端项目'",  # 您提到的例子
        "【常规】 客户端项目",
        "【常规】客户端项目",
        "常规 客户端项目",
        "常规客户端项目",
        "客户端项目",
        "js_wbmalia-研发部助理",
        "js_wbmalia 研发部助理",
        "js_wbmalia研发部助理",
        "研发部助理",
        "未知联系人",
        "其他部门"
    ]
    
    print("=== 改进的智能模糊匹配测试 ===")
    print(f"目标联系人: {target_contacts}")
    print(f"相似度阈值: {matcher.similarity_threshold}")
    print(f"算法: 字符存在性(30%) + 顺序匹配(70%)")
    print()
    
    for test_case in test_cases:
        result = matcher.match_sender(test_case)
        if result:
            target, sender, similarity = result
            print(f"✓ 匹配成功: '{test_case}' -> '{target}' (相似度: {similarity:.2f})")
        else:
            print(f"✗ 无匹配: '{test_case}'")
    
    # 详细调试几个例子
    print("\n=== 详细调试示例 ===")
    debug_cases = [
        ("j          【常规】 客户端项目                               |", "【常规】 客户端项目"),
        ("'|          【常规】 客户端项目'", "【常规】 客户端项目"),
        ("【常规】 客户端项目", "【常规】 客户端项目"),
        ("常规 客户端项目", "【常规】 客户端项目"),
        ("客户端项目", "【常规】 客户端项目"),
        ("js_wbmalia-研发部助理", "js_wbmalia-研发部助理"),
        ("js_wbmalia 研发部助理", "js_wbmalia-研发部助理")
    ]
    
    for recognized, target in debug_cases:
        matcher.debug_match_process(recognized, target)

if __name__ == "__main__":
    test_fuzzy_matcher() 