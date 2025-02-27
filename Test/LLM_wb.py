#from groq import Groq
import os
import json
from openai import OpenAI

key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=key)

def construct_kgs(text, sentences):
    """PROMPT INSPIRED BY https://arxiv.org/pdf/2407.10793"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert at creating knowledge graphs based on text.\n"
            "You will receive a long text along with all of the individual sentences of that text. You must perform the following steps on each sentence of the text, while using the context of the entire text:\n"
            "1. Entity detection: Select key and crucial entities from the sentence. Keep these entities short and concise and skip less important details of the sentence.\n"
            "2. Coreference resolution: Using the entire text, ensure that you use the same entity name for the same concept in the sentence. For example, \"He\" may actually refer to the entity \"Peter\". Also apply this step along the sentence itself.\n"
            "3. Relation extraction: Identify semantic relationships between detected entities. These relationships should be encapsulated as a simple and concise relation such as \"began in\", or \"will simulcast\", for example.\n\n"
            "Format your response as a JSON object that can be directly parsed without any edits to your response. This means that you are not allowed to include any text not part of the knowledge graphs.\n"
            "In the JSON object, there should be one element for each sentence in the text.\n"
            "Each knowledge graph should be a list of triples, with each triple being a python list of the form [\"Peter\", \"height\", \"180cm\"].\n\n"
            "See below for an example of what you should do:\n\n"},
              {"role": "user", "content":
               "Text: John Russell Reynolds (1820–1876) was an English lawyer, judge, and author. He was born in London, the son of a barrister, and was educated at Eton College and Trinity College, Cambridge. He was called to the bar in 1845, and became a Queen's Counsel in 1859. He was appointed a judge of the Court of Common Pleas in 1867, and was knighted in 1871. Reynolds was a prolific author, writing on a wide range of topics. He wrote several books on legal topics, including The Law of Libel and Slander (1863), The Law of Copyright (1865), and The Law of Patents for Inventions (1868). He also wrote on a variety of other topics, including history, biography, and literature. He was a frequent contributor to the Saturday Review, and wrote several books on Shakespeare, including The Mystery of William Shakespeare (1848) and The Authorship of Shakespeare (1875). He also wrote a biography of the poet John Keats (1848).\n"
               "Sentences: [\"John Russell Reynolds (1820–1876) was an English lawyer, judge, and author.\", \"He was born in London, the son of a barrister, and was educated at Eton College and Trinity College, Cambridge.\", \"He was called to the bar in 1845, and became a Queen's Counsel in 1859.\", \"He was appointed a judge of the Court of Common Pleas in 1867, and was knighted in 1871.\", \"Reynolds was a prolific author, writing on a wide range of topics.\", \"He wrote several books on legal topics, including The Law of Libel and Slander (1863), The Law of Copyright (1865), and The Law of Patents for Inventions (1868).\", \"He also wrote on a variety of other topics, including history, biography, and literature.\", \"He was a frequent contributor to the Saturday Review, and wrote several books on Shakespeare, including The Mystery of William Shakespeare (1848) and The Authorship of Shakespeare (1875).\", \"He also wrote a biography of the poet John Keats (1848).\" ]"
               "YOUR OUTPUT:\n"
                "{\n"
                "  \"sentence1\": [\n"
                "      [\"John Russell Reynolds\", \"born\", \"1820\"],\n"
                "      [\"John Russell Reynolds\", \"died\", \"1876\"],\n"
                "      [\"John Russell Reynolds\", \"nationality\", \"English\"],\n"
                "      [\"John Russell Reynolds\", \"occupation\", \"lawyer\"],\n"
                "      [\"John Russell Reynolds\", \"occupation\", \"judge\"],\n"
                "      [\"John Russell Reynolds\", \"occupation\", \"author\"]\n"
                "  ],\n"
                "  \"sentence2\": [\n"
                "      [\"John Russell Reynolds\", \"born in\", \"London\"],\n"
                "      [\"John Russell Reynolds\", \"son of\", \"barrister\"],\n"
                "      [\"John Russell Reynolds\", \"educated at\", \"Eton College\"],\n"
                "      [\"John Russell Reynolds\", \"educated at\", \"Trinity College\"]\n"
                "  ],\n"
                "  \"sentence3\": [\n"
                "      [\"John Russell Reynolds\", \"called to the bar\", \"1845\"],\n"
                "      [\"John Russell Reynolds\", \"became Queen's Counsel in\", \"1859\"]\n"
                "  ],\n"
                "  \"sentence4\": [\n"
                "      [\"John Russell Reynolds\", \"judge of\", \"Court of Common Pleas\"],\n"
                "      [\"John Russell Reynolds\", \"appointed judge in\", \"1867\"],\n"
                "      [\"John Russell Reynolds\", \"knighted in\", \"1871\"]\n"
                "  ],\n"
                "  \"sentence5\": [\n"
                "      [\"John Russell Reynolds\", \"called to the bar\", \"1845\"],\n"
                "      [\"John Russell Reynolds\", \"became Queen's Counsel in\", \"1859\"]\n"
                "  ],\n"
                "  \"sentence6\": [\n"
                "      [\"John Russell Reynolds\", \"occupation\", \"author\"],\n"
                "      [\"John Russell Reynolds\", \"wrote about\", \"wide range of topics\"]\n"
                "  ],\n"
                "  \"sentence7\": [\n"
                "      [\"John Russell Reynolds\", \"wrote books about\", \"legal topics\"],\n"
                "      [\"John Russell Reynolds\", \"wrote about\", \"The Law of Libel and Slander\"],\n"
                "      [\"John Russell Reynolds\", \"wrote about\", \"The Law of Copyright\"],\n"
                "      [\"John Russell Reynolds\", \"wrote about\", \"The Law of Patents for Inventions\"]\n"
                "  ],\n"
                "  \"sentence8\": [\n"
                "      [\"John Russell Reynolds\", \"wrote about\", \"history\"],\n"
                "      [\"John Russell Reynolds\", \"wrote about\", \"biography\"],\n"
                "      [\"John Russell Reynolds\", \"wrote about\", \"literature\"]\n"
                "  ],\n"
                "  \"sentence9\": [\n"
                "      [\"John Russell Reynolds\", \"was a frequent contributor to\", \"the Saturday Review\"],\n"
                "      [\"John Russell Reynolds\", \"wrote several books on\", \"Shakespeare\"]\n"
                "      [\"John Russell Reynolds\", \"wrote\", \"The Mystery of William Shakespeare\"],\n"
                "      [\"John Russell Reynolds\", \"wrote\", \"The Authorship of Shakespeare\"]\n"
                "  ],\n"
                "  \"sentence10\": [\n"
                "      [\"John Russell Reynolds\", \"wrote biography of\", \"John Keats\"]\n"
                "  ]\n"
                "}\n\n"},
                {"role": "user", "content": f"Text: {text}\nSentences: {sentences}"}
        ],
        temperature = 0
    )
    import json
    kg = response.choices[0].message.content
    return json.loads(kg)


def construct_kgs_just_text(text):
    """PROMPT INSPIRED BY https://arxiv.org/pdf/2407.10793"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert at creating knowledge graphs based on text.\n"
            "You will receive a piece of text. You must perform the following steps on the text:\n"
            "1. Entity detection: Select key and crucial entities from the text. Keep these entities short and concise and skip less important details of the text.\n"
            "2. Coreference resolution: Using the entire text, ensure that you use the same entity name for the same concept in the knowledge graph. For example, \"He\" may actually refer to the entity \"Peter\".\n"
            "3. Relation extraction: Identify semantic relationships between detected entities. These relationships should be encapsulated as a simple and concise relation such as \"began in\", or \"will simulcast\", for example.\n\n"
            "Format your response as a JSON object that can be directly parsed without any edits to your response. This means that you are not allowed to include any text not part of the knowledge graphs.\n"
            "The knowledge graph should be a list of triples, with each triple being a python list of the form [\"Peter\", \"height\", \"180cm\"].\n\n"
            "See below for an example of what you should do:\n\n"},
              {"role": "user", "content":
               "Text: John Russell Reynolds (1820–1876) was an English lawyer, judge, and author. He was born in London, the son of a barrister, and was educated at Eton College and Trinity College, Cambridge. He was called to the bar in 1845, and became a Queen's Counsel in 1859. He was appointed a judge of the Court of Common Pleas in 1867, and was knighted in 1871. Reynolds was a prolific author, writing on a wide range of topics. He wrote several books on legal topics, including The Law of Libel and Slander (1863), The Law of Copyright (1865), and The Law of Patents for Inventions (1868). He also wrote on a variety of other topics, including history, biography, and literature. He was a frequent contributor to the Saturday Review, and wrote several books on Shakespeare, including The Mystery of William Shakespeare (1848) and The Authorship of Shakespeare (1875). He also wrote a biography of the poet John Keats (1848).\n"
               "YOUR OUTPUT:\n"
                "{\n"
                "  \"knowledge graph\": [\n"
                "      [\"John Russell Reynolds\", \"born\", \"1820\"],\n"
                "      [\"John Russell Reynolds\", \"died\", \"1876\"],\n"
                "      [\"John Russell Reynolds\", \"nationality\", \"English\"],\n"
                "      [\"John Russell Reynolds\", \"occupation\", \"lawyer\"],\n"
                "      [\"John Russell Reynolds\", \"occupation\", \"judge\"],\n"
                "      [\"John Russell Reynolds\", \"occupation\", \"author\"],\n"
                "      [\"John Russell Reynolds\", \"born in\", \"London\"],\n"
                "      [\"John Russell Reynolds\", \"son of\", \"barrister\"],\n"
                "      [\"John Russell Reynolds\", \"educated at\", \"Eton College\"],\n"
                "      [\"John Russell Reynolds\", \"educated at\", \"Trinity College\"],\n"
                "      [\"John Russell Reynolds\", \"called to the bar\", \"1845\"],\n"
                "      [\"John Russell Reynolds\", \"judge of\", \"Court of Common Pleas\"],\n"
                "      [\"John Russell Reynolds\", \"appointed judge in\", \"1867\"],\n"
                "      [\"John Russell Reynolds\", \"knighted in\", \"1871\"],\n"
                "      [\"John Russell Reynolds\", \"became Queen's Counsel in\", \"1859\"],\n"
                "      [\"John Russell Reynolds\", \"occupation\", \"author\"],\n"
                "      [\"John Russell Reynolds\", \"wrote about\", \"wide range of topics\"],\n"
                "      [\"John Russell Reynolds\", \"wrote books about\", \"legal topics\"],\n"
                "      [\"John Russell Reynolds\", \"wrote about\", \"The Law of Libel and Slander\"],\n"
                "      [\"John Russell Reynolds\", \"wrote about\", \"The Law of Copyright\"],\n"
                "      [\"John Russell Reynolds\", \"wrote about\", \"The Law of Patents for Inventions\"],\n"
                "      [\"John Russell Reynolds\", \"wrote about\", \"history\"],\n"
                "      [\"John Russell Reynolds\", \"wrote about\", \"biography\"],\n"
                "      [\"John Russell Reynolds\", \"wrote about\", \"literature\"],\n"
                "      [\"John Russell Reynolds\", \"was a frequent contributor to\", \"the Saturday Review\"],\n"
                "      [\"John Russell Reynolds\", \"wrote several books on\", \"Shakespeare\"]\n"
                "      [\"John Russell Reynolds\", \"wrote\", \"The Mystery of William Shakespeare\"],\n"
                "      [\"John Russell Reynolds\", \"wrote\", \"The Authorship of Shakespeare\"],\n"
                "      [\"John Russell Reynolds\", \"wrote biography of\", \"John Keats\"]\n"
                "  ]\n"
                "}\n\n"},
                {"role": "user", "content": f"Text: {text}"}
        ],
        temperature = 0
    )
    import json
    kg = response.choices[0].message.content
    return json.loads(kg)

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