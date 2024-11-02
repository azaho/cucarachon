from flask import Flask, request, jsonify, render_template_string
import openai
from openai import OpenAI
import os

app = Flask(__name__)

# Set your OpenAI API key
api_key_openai = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key_openai
client = OpenAI(
    # This is the default and can be omitted
    api_key=api_key_openai)


@app.route('/')
def homepage():
    # Render a simple HTML form for the user interface
    with open('homepage.html', 'r') as f:
        html_content = f.read()
    return render_template_string(html_content)


@app.route('/process', methods=['GET'])
def process_request():
    # Extract the array of arrays from the request parameters
    array_of_arrays = request.args.getlist('data', type=str)
    if not array_of_arrays:
        return jsonify(
            {'error': 'Invalid input: parameter "data" is required.'}), 400

    try:
        # Convert parameter to array of arrays
        array_of_arrays = eval(array_of_arrays[0])
    except Exception as e:
        return jsonify({
            'error':
            'Invalid format for parameter "data". Expecting an array of arrays.'
        }), 400

    try:
        # Import itertools for generating combinations
        from itertools import product
        
        # Generate all possible combinations taking one item from each array
        all_combinations = list(product(*array_of_arrays))
        
        # Store results for each combination
        all_results = []
        all_summaries = []
        all_evaluations = []
        all_jsons = []
        
        # Process each combination
        for combination in all_combinations:
            result, summary_result, evaluation_result, json_result = generate_startup_idea(list(combination))
            all_results.append(result)
            all_summaries.append(summary_result) 
            all_evaluations.append(evaluation_result)
            all_jsons.append(json_result)
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({
        'results': all_results,
        'summaries': all_summaries, 
        'evaluations': all_evaluations,
        'jsons': all_jsons
    })


def generate_startup_idea(array_of_arrays, temperature=0.7):
    # Move prompts to a separate file for maintainability
    from prompts import startup_prompt, summary_prompt_template, evaluation_prompt_template, json_format_prompt_template

    print(f"EVALUATING {array_of_arrays}")

    # Read the pitch evaluation metric from the txt file
    with open("pitch_evaluation_metric.txt", "r") as f:
        pitch_evaluation_metric = f.read()

    # Generate the startup idea
    prompt = startup_prompt.format(array_of_arrays=array_of_arrays)

    # Call the OpenAI GPT-4o mini model
    response = client.chat.completions.create(messages=[{
        "role": "user",
        "content": prompt,
    }],
                                              model="gpt-4o-mini",
                                              temperature=temperature)
    result = response.choices[0].message.content

    # Generate a follow-up to summarize in a pitch format
    summary_prompt = summary_prompt_template.format(result=result)
    summary_response = client.chat.completions.create(messages=[{
        "role": "user",
        "content": summary_prompt,
    }],
                                                      model="gpt-4o-mini",
                                                      temperature=temperature)
    summary_result = summary_response.choices[0].message.content

    # Evaluate the pitch based on the given metric
    evaluation_prompt = evaluation_prompt_template.format(
        summary_result=summary_result, metric=pitch_evaluation_metric)
    evaluation_response = client.chat.completions.create(messages=[{
        "role": "user",
        "content": evaluation_prompt,
    }],
                                                         model="gpt-4o-mini",
                                                         temperature=temperature)
    evaluation_result = evaluation_response.choices[0].message.content

    # Convert the evaluation result to a JSON array of numbers
    json_format_prompt = json_format_prompt_template.format(evaluation_result=evaluation_result)
    json_response = client.chat.completions.create(messages=[{
        "role": "user",
        "content": json_format_prompt,
    }],
                                                   model="gpt-4o-mini",
                                                   temperature=temperature)
    json_result = json_response.choices[0].message.content

    print(evaluation_result, json_result, "\n\n\n\n\n\n")

    return result, summary_result, evaluation_result, json_result


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

