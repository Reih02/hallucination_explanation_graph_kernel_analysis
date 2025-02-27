from groq import Groq
import os
import json
from openai import OpenAI

key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=key)

def final_kg_constructor(text1, text2):
    sample_text1 = "A&E Networks will simulcast the original \"Roots\" in 2016. The original \"Roots\" premiered in 1977 and ran for four seasons. The miniseries followed Kunta Kinte, a free black man in Virginia, as he was sold into slavery."
    sample_text2 = "(CNN)One of the biggest TV events of all time is being reimagined for new audiences. \"Roots,\" the epic miniseries about an African-American slave and his descendants, had a staggering audience of over 100 million viewers back in 1977"
    sample_text3 = "ISIS released more than 200 Yazidis, a minority group, a group says. The Islamist terror group has been killed in recent summer. ISIS released scores of other Yazidis, mainly children and the elderly. The Peshmerga commander says the freed Yazidis are released."
    sample_text4 = "(CNN) ISIS on Wednesday released more than 200 Yazidis, a minority group whose members were killed, captured and displaced when the Islamist terror organization overtook their towns in northern Iraq last summer, officials said. Most of those released were women and children; the rest were ill or elderly, said Rassol Omar, a commander in the Peshmerga force that defends northern Iraq's semi-autonomous Kurdish region. Omar didn't say what led to the release, other than asserting that Arab tribal leaders helped to coordinate it. The freed Yazidis were received by Peshmerga, who sent them to the Kurdish regional capital, Irbil, said Nuri Osman, an official with Iraq's Kurdistan Regional Government. It wasn't immediately clear what motivated Wednesday's release, Osman said."
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    #model="llama3-8b-8192",
    messages=[
        {"role": "system", "content": "You are an expert at creating knowledge graphs based on text.\n"
         "You will receive two separate pieces of text, and you must perform the following steps on each piece of text:\n"
         "1. Entity detection: Select key and crucial entities from the text. Keep these entities short and concise and skip less important details of the textn\n"
         "2. Coreference resolution: Across both texts, ensure that you use the same entity name for the same concept. For example, \"He\" may actually refer to the entity \"Peter\". Also apply this step between texts, so that the two knowledge graphs can be compared as easily as possible without confusion.\n"
         "3. Relation extraction: Identify semantic relationships between detected entities. These relationships should be encapsulated as a simple and concise relation such as \"began in\", or \"will simulcast\", for example.\n"
         "4. Knowledge Graph refinement: Once the two knowledge graphs have been created, try to ensure that similar triples between the two texts / knowledge graphs are represented the same way, to avoid confusion. For example, if two different entities refer to a similar event or concept, relabel them to be the same across the two knowledge graphs.\n\n"
         "Format your response as a JSON object that can be directly parsed without any edits to your response. This means that you are not allowed to include any text not part of the knowledge graphs.\n"
         "In the JSON object, one element should be the knowledge graph for the first text, and another element should be the knowledge graph for the second text.\n"
         "Each knowledge graph should be a list of triples, with each triple being a python list of the form [\"Peter\", \"height\", \"180cm\"].\n\n"
         "See below for some examples:\n\n"
         "EXAMPLE 1:\n"
         f"TEXT1: \n{sample_text1}\n\nTEXT2:\n{sample_text2}\n\n"
         "YOUR OUTPUT:\n"
         "{\n"
         "  \"knowledge_graph1\": [\n"
         "      [\"A&E Networks\", \"will simulcast in 2016\", \"Roots\"],\n"
         "      [\"Roots\", \"premiered in\", \"1977\"],\n"
         "      [\"Roots\", \"ran for\", \"four seasons\"],\n"
         "      [\"Roots\", \"instance of\", \"miniseries\"],\n"
         "      [\"Roots\", \"followed\", \"Kunta Kinte\"],\n"
         "      [\"Kunta Kinte\", \"was sold into\", \"slavery\"],\n"
         "      [\"Kunta Kinte\", \"was a\", \"free black man\"]\n"
         "  ],\n"
         "  \"knowledge_graph2\": [\n"
         "      [\"Roots\", \"one of the\", \"biggest TV events of all time\"],\n"
         "      [\"Roots\", \"had a staggering audience of\", \"over 100 million viewers\"],\n"
         "      [\"Roots\", \"being\", \"reimagined for new audiences\"],\n"
         "      [\"Roots\", \"was about\", \"an African-American slave and his descendants\"],\n"
         "      [\"Roots\", \"premiered\", \"1977\"]\n"
         "  ]\n"
         "}\n\n"

         "EXAMPLE 2:\n"
         f"TEXT1: \n{sample_text3}\n\nTEXT2:\n{sample_text4}\n\n"
         "YOUR OUTPUT:\n"
         "{\n"
         "  \"knowledge_graph1\": [\n"
         "      [\"ISIS\", \"released\", \"more than 200 Yazidis\"],\n"
         "      [\"Yazidis\", \"are\", \"minority group\"],\n"
         "      [\"ISIS\", \"released\", \"children and elderly Yazidis\"],\n"
         "      [\"Peshmerga commander\", \"said\", \"freed Yazidis are released\"]\n"
         "  ],\n"
         "  \"knowledge_graph2\": [\n"
         "      [\"ISIS\", \"released\", \"more than 200 Yazidis\"],\n"
         "      [\"Yazidis\", \"are\", \"minority group\"],\n"
         "      [\"Yazidis\", \"killed and displaced by\", \"ISIS\"],\n"
         "      [\"ISIS\", \"released\", \"children and elderly Yazidis\"],\n"
         "      [\"Peshmerga commander\", \"said\", \"freed Yazidis are released\"]\n"
         "      [\"Peshmerga\", \"received\", \"freed Yazidis\"],\n"
         "      [\"Peshmerga\", \"sent freed Yazidis to\", \"Irbil\"],\n"
         "      [\"Arab tribal leaders\", \"helped coordinate\", \"release of Yazidis\"]\n"
         "  ]\n"
         "}"},
         {"role": "user", "content": f"TEXT1: \n{text1}\n\nTEXT2:\n{text2}"}
    ],
    temperature=0
    )
    kg = response.choices[0].message.content
    return kg

def explain_ged_operations(summary, context, explanations):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Your task is to generate a contrastive explanation as to why a knowledge graph produced from an LLM's output contains an hallucination.\n"
             "To achieve this task, you will receive a list of explanations obtained from running a graph edit distance algorithm between the LLM's output knowledge graph and a ground truth knowledge graph.\n"
             "This list of explanations shows the steps needed to transform the LLM's output knowledge graph into the ground truth knowledge graph, effectively capturing the hallucinatory components of the LLM's output.\n"
             "Instead of listing off each hallucination, try to tie it together into a paragraph to discuss the key false claims that the LLM's output knowledge graph contains.\n"
             "You will also receieve the LLM's output text, and the original context that the LLM used to generate the summary of. Use context and common-sense from these three pieces of information to guide your explanation"},
            {"role": "user", "content": f"###Context###:\n{context}\n\n###LLM summary/output###:\n{summary}\n\n###Explanations###:\n{explanations}"}
        ],
        temperature=0
    )
    content = response.choices[0].message.content
    return content

    
