# prompts.py

startup_prompt = """
You are a creative startup engineer looking to combine the elements below into the most possibly viable idea for a startup, that has a market waiting for it, and is realistic to do!

aspects:
{array_of_arrays}
"""




summary_prompt_template = """
Summarize the following startup idea into a one-paragraph pitch, including the main details about the market size, opportunity, value proposition, and why the idea is realistic. Do not make up a name for the startup, just say what it does.

{result}
"""




evaluation_prompt_template = """
Please evaluate the following pitch based on the provided multi-dimensional metric. The metric includes several considerations, such as uniqueness, market potential, scalability, feasibility, and potential impact.

Pitch:
{summary_result}

Evaluation Criteria:
{metric}

Provide a detailed evaluation of the pitch according to these criteria, highlighting strengths, weaknesses, and suggestions for improvement. Make sure to NOT be sycophantic, and be honest. don't give all maximum or top scores.
"""


# Example of json_format_prompt_template
json_format_prompt_template = """
Please convert the following evaluation into a JSON array format, where each value is a numerical score between 1 and 5 representing different aspects of the evaluation.

Evaluation:
{evaluation_result}

Output the result as a JSON array of numbers only, without any additional text or explanation. Don't output the code block format, just output the raw JSON array so that I can immediately use the output.
"""
evaluation_name_strings = ["Market Potential", "Scalability", "Feasibility", "Customer Need", "Revenue Model"]