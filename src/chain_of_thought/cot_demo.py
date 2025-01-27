from src.llm_client.azure_client import AzureClient


class CognitiveFlow:
    def __init__(self):
        """Initialize the cognitive flow with an AzureClient instance."""
        self.azure_client = AzureClient()

    def break_down_query(self, query):
        """Break down the query into 3 specific sub-questions."""
        system_prompt = """
        你是一名具有逻辑思维能力的分析师，擅长将复杂问题分解为清晰的步骤。
        请将以下问题拆解成3个具体的子问题，并确保问题之间是逻辑连贯的。每个问题应该简洁且具有针对性。
        """
        user_prompt = f"问题：{query}"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        return self.azure_client.call_azure_openai(messages)

    def answer_sub_questions(self, sub_questions):
        """Answer the sub-questions step by step."""
        answers = []
        for sub_question in sub_questions:
            system_prompt = """
            你是一名经验丰富的顾问，专注于商业和经济领域。请根据以下子问题提供详细、专业的回答。
            """
            user_prompt = f"问题：{sub_question}"

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]

            answer = self.azure_client.call_azure_openai(messages)
            answers.append(answer)

        return answers

    def summarize_answers(self, answers):
        """Summarize the answers into a concise conclusion."""
        system_prompt = """
        你是一名总结专家，擅长从多个答案中提炼出简洁、清晰的结论。请根据以下回答总结出一个简洁的结论。
        """
        user_prompt = "\n".join([f"回答 {i + 1}: {ans}" for i, ans in enumerate(answers)])

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        return self.azure_client.call_azure_openai(messages)

    def process_query(self, query):
        """Process the entire query: break it down, answer sub-questions, and summarize."""
        # Step 1: Break down the query
        print("步骤 1: 拆解问题...")
        sub_questions = self.break_down_query(query)
        print(f"拆解出的子问题:\n{sub_questions}\n")

        # Split the sub-questions into a list
        sub_questions_list = sub_questions.split("\n")

        # Step 2: Answer the sub-questions
        print("步骤 2: 逐步回答子问题...")
        answers = []
        for i, sub_question in enumerate(sub_questions_list, 1):
            print(f"正在回答子问题 {i}: {sub_question}")
            answers += self.answer_sub_questions([sub_question])
            print(f"回答 {i}: {answers[-1]}\n")

        # Step 3: Summarize the answers
        print("步骤 3: 总结回答...")
        summary = self.summarize_answers(answers)
        print(f"总结：\n{summary}")

if __name__ == "__main__":
    # Initialize the CognitiveFlow agent
    cognitive_flow = CognitiveFlow()
    query = input("请输入想知道的内容:\n ")
    # Sample query
    # query = "中国的十大富豪，及其公司、财富和经验是什么？"

    # Process the query
    cognitive_flow.process_query(query)