import os
import openai
import readline

openai.api_key = os.getenv("OPENAI_API_KEY")

prompt_file_path = "./prompts/1.txt"
with open(prompt_file_path, "r") as f:
    prompt = f.read()

article_file_path = "./articles/1.txt"
with open(article_file_path, "r") as f:
    article = f.read()


def create_summary(article):
    response = openai.ChatCompletion.create(
        model = "gpt-4",
        messages = [
            {"role": "user", "content": "Please summarize the following article in Japanese: \n\n" + article},
        ],
        temperature = 1,
        max_tokens = 256,
    )

    response_text = response.choices[0].message.content
    return response_text


def answer_question(question_from_gpt, article):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": "Please answer the following question briefly by reading the article in Japanese.: \n\n" + question_from_gpt + "\n\n article: \n\n" + article},
        ],
        temperature=1,
        max_tokens=256,
    )

    response_text = response.choices[0].message.content
    return response_text


def is_question(response_from_gpt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": "If the following sentence is a question, reply with 'Yes'. If not, reply with 'No'. \n\n" + response_from_gpt},
        ],
        temperature=0,
        max_tokens=256,
    )

    response_text = response.choices[0].message.content
    upper_response_text = response_text.upper()

    if "YES" in upper_response_text:
        return True
    else:
        return False


def get_first_question(summary, article):
    response = openai.ChatCompletion.create(
        model = "gpt-4",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": "This is an article I want to study: \n\n" + article},
            {"role": "user", "content": "Please ask questions to the following sumary: \n\n" + summary},
        ],
        temperature = 0,
        max_tokens = 256,
    )

    response_text = response.choices[0].message.content
    return response_text


def main():
    history = []
    summary = create_summary(article)
    print("概要: " + summary)
    print()
    question_from_gpt = get_first_question(summary, article)
    print("生徒(GPT): " + question_from_gpt)
    print()

    while True:
        answer = answer_question(question_from_gpt, article)
        print("先生(User): " + answer)
        print()

        input("Press Enter to continue...")

        response = openai.ChatCompletion.create(
            model = "gpt-4",
            messages=[
                {"role": "system", "content": prompt},
                *history,
                {"role": "user", "content": answer},
            ],
            temperature = 0,
            max_tokens = 256,
        )

        response_text = response.choices[0].message.content
        print("生徒(GPT): " + response_text)

        history.append({"role": "user", "content": answer})
        history.append({"role": "assistant", "content": response_text})

        if not is_question(response_text):
            print("response is not a question")
            break

        question_from_gpt = response_text


if __name__ == "__main__":
    main()
