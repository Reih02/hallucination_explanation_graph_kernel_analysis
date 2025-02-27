from groq import Groq
import os
import json
from openai import OpenAI

key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=key)

# def construct_kgs(text):
#     response = client.chat.completions.create(
#         model="llama3-8b-8192",
#         messages=[
#             {"role": "system", "content": "Please ensure that your response is well-structured, concise, and free of infinite or excessive repetitions. Your response should not contain repeating elements or duplicate entries. Keep the response under 10,000 characters.\n"
#                       "Your task is to create knowledge graphs based on some text.\n"
#                       "You will be given a piece of text (delimited by ###).\n"
#                       "You need to extract entities and relations from this text.\n"
#                       "Entities can be key parts of the text, such as people, places, subjects, objects, etc.\n"
#                       "Relations should encapsulate the context and meaning of the text and be in the form of (subject, relation, object).\n"
#                       "Ensure that each relation has exactly three components, with each component consisting of a single string (i.e no lists etc.), and avoid duplications in both entities and relations.\n"
#                       "Duplicates are entries with the same value in either list. For example, if 'Canada' appears more than once, remove the duplicates.\n"
#                       "Return your response in a proper JSON format (that is properly finished) with two lists: one for entities and one for relations. For example:\n"
#                       "###The sky is blue, planes fly in the sky###\n\n"
#                       "{\n"
#                       "  \"entities\": [\"sky\", \"blue\", \"plane\", \"fly\"],\n"
#                       "  \"relations\": [\n"
#                       "    [\"sky\", \"is\", \"blue\"],\n"
#                       "    [\"plane\", \"flies in\", \"sky\"]\n"
#                       "  ],\n"
#                       "}\n"},
#             {"role": "user", "content": f"###{text}###\n\n"}
#         ],
#         temperature = 0
#     )
#     content = response.choices[0].message.content
#     try:
#         parsed_response = json.loads(content)
#         return parsed_response
#     except json.JSONDecodeError as e:
#         # print("###CONSTRUCT_KGS()###")
#         # #print(f"Input: {text}")
#         # print(f"Error parsing JSON response: {e}")
#         # print(f"Content: {content}")
#         return fix_json_response(content)



def construct_kgs_simultaneous(text1, text2):
    response = client.chat.completions.create(
    model="llama-3.1-70b-versatile",
    messages=[
        {"role": "system", "content": "You are an expert at extracting information from text into a structured format in order to build a knowledge graph.\n"
         "You will receive two separate pieces of text. Your job is to perform the following steps with each piece of text:\n"
         "Step 1: Entity detection - Identify all entities in the raw text. Entities should be basic and simple, they are akin to Wikipedia nodes.\n"
         "Step 2: Coreference resolution - Both within each text and between both texts, find all expressions in the texts that refer to the same entity. Make sure entities are not duplicated. In particular do not include entities that are more specific versions of themselves, e.g 'a detailed view of jupiter's atmosphere' and 'jupiter's atmosphere', only include the most specific version of the entity.\n"
         "Step 3: Relation extraction - Identify semantic relationships between the entities you have identified.\n"
         "Format your output as a **Python tuple** (surrounded by a <python> and </python> tag) containing two lists of triples (i.e [entity1, relation1-2, entity2]) for each text. Ensure your output is in Python code. Do not return anything in your output except for this python code, as your raw output will be converted to a python list.\n"
         "Return a tuple, with the first element being the knowledge graph for the first text, and the second element being the knowledge graph for the second text.\n"},
         {"role": "system", "content": "See below for some examples of input and output, so that you get a better feel of what to do:\n\n"
         "Text 1: 'John Russell Reynolds (1820–1876) was an English lawyer, judge, and author.'\n"
         "Text 2: 'He was born in London and educated at Eton College and Trinity College, Cambridge.'\n"
         "Output:\n"
         "<python>([['John Russell Reynolds', 'born', '1820'],['John Russell Reynolds', 'died', '1876'],['John Russell Reynolds', 'nationality', 'England'],['John Russell Reynolds', 'occupation', 'lawyer'],['John Russell Reynolds', 'occupation', 'judge'],['John Russell Reynolds', 'occupation', 'author']],[['John Russell Reynolds', 'birthplace', 'London'],['John Russell Reynolds', 'educated at', 'Eton College'],['John Russell Reynolds', 'educated at', 'Trinity College']])</python>\n"},
         {"role": "user", "content": f"Text 1: {text1}\nText 2: {text2}\n\n"}
    ],
    temperature=0
    )
    kg = response.choices[0].message.content
    
    # import ast
    # try:
    #     kg_parsed = ast.literal_eval(kg)
    # except:
    #     response = client.chat.completions.create(
    #     model="llama3-8b-8192",
    #     messages=[
    #         {"role": "system", "content": "Your job is to take a string from an LLM, and ensure that it is able to be parsed using ast.literal_eval(string) in python.\n"
    #          "IMPORTANT: It is crucial that you do not modify the semantic meaning of any of the triples in the knowledge graphs.\n"
    #          "Return your response as purely content able to be parsed in python, as I will directly copy all of your output and parse it using ast.literal_eval(). This means you should not include any pre-amble or explanation of what you did.\n"},
    #          {"role": "user", "content": f"Here is the string: {kg}"}
    #     ],
    #     temperature=0
    #     )
    #     kg = response.choices[0].message.content
    #     kg_parsed = ast.literal_eval(kg)

    return kg

def final_kg_constructor(text1, text2):
    sample_text1 = "A diet rich in oily fish, whole grains, lean protein, fruit and vegetables should provide enough nutrients."
    sample_text2 = "Vitamin and mineral supplements are becoming more and more popular as health conscious shoppers focus on good nutrition, but do we really need pills to optimise our diet? Not according to nutritionist and author sarah flower, who says that cooking with the right ingredients should give you all the goodness you need. ` the cleaner your diet - using fresh ingredients and cooking at home - the less likely you are to need to rely on supplements to boost your health.' She told mailonline. Scroll down for video. It's time to ditch vitamin pills for a diet rich in clean, fresh and unprocessed foods, says sarah flower. ` the typical western diet is heavily processed and sugar ridden,' explains sarah, `this makes us more susceptible to vitamin and mineral deficiencies.' And while it may seem like common sense to eat more unprocessed and raw foods, ms flower believes we are still not doing enough. ` we are living in a society where it is possible to be overweight and deficient in essential nutrients.' She continued.' A diet rich in oily fish, whole grains, lean protein, fruit and vegetables should provide enough nutrients,' she said. Other factors to consider include your ability to absorb the food - digestive complaints can often impede our ability to absorb nutrients. ` pregnancy, ill health and the elderly may need more support,' she said. And menstruating women may benefit from adding oils ( evening primrose oil ) and a multivitamin rich in magnesium to help alleviate pms symptoms ( ms flowers recommends magnesium citrate ). Always opt for steaming over boiling vegetables and eat as many raw pieces as you can every day. ` fruit and vegetables not only contain vitamins but also vital phytonutrients, which have an amazing ability to protect us against degenerative diseases such as cancer, alzheimer's and heart disease,'"
    sample_text3 = "Doyne, nepal, met women and children in nepal."
    sample_text4 = "Surkhet, nepal ( cnn ) ten years ago, with her high school diploma and a backpack, maggie doyne left her new jersey hometown to travel the world before college. She lived in a buddhist monastery, helped rebuild a sea wall in fiji, then went to india and worked with nepalese refugees. There, she met a young girl who wanted to find her family in nepal. Doyne went with her. That's when doyne's life took an unexpected turn. Do you know a hero? Nominations are open for cnn heroes 2015. A decade - long civil war had just ended in the country, and doyne witnessed its effects firsthand. She met women and children who were suffering, struggling to survive. ` `it changed me,'' said doyne, now 28. ` `there were children with mallets that would go into the riverbed, pick up a big stone and break it into little, little pieces ( to sell ). And they were doing that all day, every day.' ' doyne called her parents and asked them to wire her the $ 5, 000 she had earned babysitting. In 2006, she purchased land in surkhet, a district in western nepal. She worked for two years with the local community to build the kopila valley children's home. Today, kopila - - which means `` flower bud'' in nepali - - is home to about 50 children, from infants to teenagers. Doyne started the blinknow foundation to support and grow her efforts. In 2010, the group opened its kopila valley school, which today educates more than 350 students. Doyne lives in nepal year - round, traveling to the u. S. A few times a year. See more cnn heroes. The cnn heroes team traveled to surkhet and talked to doyne about her work and the community she supports. Below"
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
         "      [\"diet\", \"rich in oily fish, whole grains, lean protein, fruit, and vegetables\", \"should provide enough nutrients\"]\n"
         "  ],\n"
         "  \"knowledge_graph2\": [\n"
         "      [\"sarah flower\", \"says\", \"cooking with the right ingredients should give you all the goodness you need\"],\n"
         "      [\"sarah flower\", \"says\", \"the cleaner your diet is, the less likely you are to need supplements\"],\n"
         "      [\"diet\", \"rich in oily fish, whole grains, lean protein, fruit, and vegetables\", \"should provide enough nutrients\"],\n"
         "      [\"sarah flower\", \"explains\", \"the typical western diet is heavily processed and sugar ridden\"],\n"
         "      [\"sarah flower\", \"believes\", \"we are still not doing enough to eat unprocessed and raw foods\"],\n"
         "      [\"sarah flower\", \"says\", \"pregnancy, ill health and the elderly may need more support\"],\n"
         "      [\"sarah flower\", \"recommends\", \"magnesium citrate for menstruating women\"],\n"
         "      [\"fruit and vegetables\", \"contain\", \"vitamins\"],\n"
         "      [\"fruit and vegetables\", \"contain\", \"phytonutrients\"],\n"
         "      [\"phytonutrients\", \"protect against\", \"degenerative diseases\"]\n"
         "  ]\n"
         "}\n\n"

         "EXAMPLE 2:\n"
         f"TEXT1: \n{sample_text3}\n\nTEXT2:\n{sample_text4}\n\n"
         "YOUR OUTPUT:\n"
         "{\n"
         "  \"knowledge_graph1\": [\n"
         "      [\"Doyne\", \"met\", \"women and children\"],\n"
         "      [\"Doyne\", \"is in\", \"Nepal\"]\n"
         "  ],\n"
         "  \"knowledge_graph2\": [\n"
        "       [\"Maggie Doyne\", \"left\", \"New Jersey hometown\"],\n"
        "       [\"Maggie Doyne\", \"traveled to\", \"world before college\"],\n"
        "       [\"Maggie Doyne\", \"lived in\", \"Buddhist monastery\"],\n"
        "       [\"Maggie Doyne\", \"helped rebuild\", \"sea wall in Fiji\"],\n"
        "       [\"Maggie Doyne\", \"worked with\", \"Nepalese refugees in India\"],\n"
        "       [\"Maggie Doyne\", \"met\", \"young girl who wanted to find her family in Nepal\"],\n"
        "       [\"Maggie Doyne\", \"went with\", \"young girl to Nepal\"],\n"
        "       [\"Maggie Doyne\", \"witnessed\", \"effects of decade-long civil war in Nepal\"],\n"
        "       [\"Maggie Doyne\", \"saw\", \"women and children suffering in Nepal\"],\n"
        "       [\"Maggie Doyne\", \"saw\", \"children breaking stones to sell\"],\n"
        "       [\"Maggie Doyne\", \"asked parents for\", \"$5,000\"],\n"
        "       [\"Maggie Doyne\", \"purchased\", \"land in Surkhet, Nepal\"],\n"
        "       [\"Maggie Doyne\", \"built\", \"Kopila Valley Children's Home\"],\n"
        "       [\"Kopila Valley Children's Home\", \"is home to\", \"about 50 children\"],\n"
        "       [\"Kopila Valley Children's Home\", \"provides care for\", \"infants to teenagers\"],\n"
        "       [\"Maggie Doyne\", \"started\", \"BlinkNow Foundation\"],\n"
        "       [\"BlinkNow Foundation\", \"opened\", \"Kopila Valley School in 2010\"],\n"
        "       [\"Kopila Valley School\", \"educates\", \"more than 350 students\"],\n"
        "       [\"Maggie Doyne\", \"lives in\", \"Nepal year-round\"],\n"
        "       [\"Maggie Doyne\", \"travels to\", \"USA a few times a year\"],\n"
        "       [\"CNN Heroes team\", \"traveled to\", \"Surkhet to interview Maggie Doyne\"],\n"
        "       [\"CNN Heroes team\", \"talked to\", \"Maggie Doyne about her work and the community\"]\n"
        "  ]\n"
        "}"},
         {"role": "user", "content": f"TEXT1: \n{text1}\n\nTEXT2:\n{text2}"}
    ],
    temperature=0
    )
    kg = response.choices[0].message.content
    return kg

# text1 = "Surkhet, nepal ( cnn ) ten years ago, with her high school diploma and a backpack, maggie doyne left her new jersey hometown to travel the world before college. She lived in a buddhist monastery, helped rebuild a sea wall in fiji, then went to india and worked with nepalese refugees. There, she met a young girl who wanted to find her family in nepal. Doyne went with her. That's when doyne's life took an unexpected turn. Do you know a hero? Nominations are open for cnn heroes 2015. A decade - long civil war had just ended in the country, and doyne witnessed its effects firsthand. She met women and children who were suffering, struggling to survive. ` `it changed me,'' said doyne, now 28. ` `there were children with mallets that would go into the riverbed, pick up a big stone and break it into little, little pieces ( to sell ). And they were doing that all day, every day.' ' doyne called her parents and asked them to wire her the $ 5, 000 she had earned babysitting. In 2006, she purchased land in surkhet, a district in western nepal. She worked for two years with the local community to build the kopila valley children's home. Today, kopila - - which means `` flower bud'' in nepali - - is home to about 50 children, from infants to teenagers. Doyne started the blinknow foundation to support and grow her efforts. In 2010, the group opened its kopila valley school, which today educates more than 350 students. Doyne lives in nepal year - round, traveling to the u. S. A few times a year. See more cnn heroes. The cnn heroes team traveled to surkhet and talked to doyne about her work and the community she supports. Below"
# text2 = "Doyne, nepal, met women and children in nepal."
# output = final_kg_constructor(text2, text1)
# KGs = json.loads(output)

# claim_kg = KGs["knowledge_graph1"]
# context_kg = KGs["knowledge_graph2"]

# print(f"### CLAIM ###:\n{claim_kg}\n\n### CONTEXT ###:\n{context_kg}")

def sandbox_kgs_test(text1, text2):
    example_text1 = (
        "ISIS released more than 200 Yazidis, a minority group, a group says. "
        "The Islamist terror group has been killed in recent summer. "
        "ISIS released scores of other Yazidis, mainly children and the elderly. "
        "The Peshmerga commander says the freed Yazidis are released."
    )
    example_text2 = (
        "(CNN) ISIS on Wednesday released more than 200 Yazidis, a minority group whose members were killed, "
        "captured and displaced when the Islamist terror organization overtook their towns in northern Iraq last summer, officials said. "
        "Most of those released were women and children; the rest were ill or elderly, said Rassol Omar, a commander in the Peshmerga force "
        "that defends northern Iraq's semi-autonomous Kurdish region. Omar didn't say what led to the release, other than asserting that Arab "
        "tribal leaders helped to coordinate it. The freed Yazidis were received by Peshmerga, who sent them to the Kurdish regional capital, Irbil, "
        "said Nuri Osman, an official with Iraq's Kurdistan Regional Government. It wasn't immediately clear what motivated Wednesday's release, "
        "Osman said. Osman said 217 Yazidis were released. Omar, the Peshmerga commander, had a higher count: 228. "
        "ISIS previously released scores of other Yazidis -- largely children and the elderly -- since attacking the group's towns last year. "
        "The Sunni Islamist militant group steamrolled into Iraq's north last summer, forcing hundreds of thousands of minorities -- Yazidis among them -- "
        "from their homes. Yazidis are of Kurdish descent, and their religion is considered a pre-Islamic sect that draws from Christianity, Judaism and Zoroastrianism. "
        "One of the oldest religious communities in the world, the Yazidis have long suffered persecution, with many Muslims referring to them as devil worshipers. "
        "ISIS' cruelty to them has been extraordinary. ISIS' conquest of the town of Sinjar, in particular, provoked a major humanitarian crisis as some Yazidis fled "
        "into the mountains -- where many became trapped for a time without food and water -- and others fled by foot into neighboring Syria. "
        "ISIS slaughtered Yazidis by the hundreds, Yian Dakhil, the only lawmaker representing the Yazidis in Iraq's Parliament, told CNN last year. "
        "Reports emerged from some Yazidi survivors that ISIS raped and enslaved female Yazidi captives. "
        "An international coalition responded, first by airdropping supplies in the mountains. Rescues came next. And then, starting in August, the United States "
        "and other nations conducted airstrikes targeting ISIS in Iraq and Syria. The U.S. State Department estimates that 500,000 Yazidis live in northern Iraq, "
        "accounting for less than 1 percent of the country's population. CNN's Raja Razek reported from Beirut. CNN's Jason Hanna wrote from Atlanta. CNN's Hamdi Alkshali, "
        "Faith Karimi and Yousuf Basil contributed to this report."
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert at creating detailed and accurate knowledge graphs based on text. "
                    "Your task is to analyze two pieces of text and perform the following steps:\n\n"
                    "1. **Entity Detection**: Identify key entities from the text, such as people, places, organizations, events, "
                    "and concepts. Exclude unimportant details. Keep the entities concise and standardized.\n"
                    "2. **Coreference Resolution**: Resolve coreferences within and between the texts. Ensure the same entity name "
                    "is used for identical concepts across the knowledge graphs to avoid inconsistency.\n"
                    "3. **Relation Extraction**: Extract semantic relationships between detected entities. Relations should "
                    "be brief and meaningful, e.g., \"released by\", \"premiered in\", \"located in\".\n"
                    "4. **Graph Alignment**: Ensure that overlapping or similar triples in both texts are represented identically. "
                    "Merge triples if necessary for clarity and avoid redundancy.\n\n"
                    "Output the result as a JSON object containing two elements: 'knowledge_graph1' for the first text and "
                    "'knowledge_graph2' for the second. Each knowledge graph is a list of triples, where each triple is a list in "
                    "the format [\"Entity1\", \"Relation\", \"Entity2\"].\n\n"
                    "Here is an example:\n\n"
                    f"TEXT1:\n{example_text1}\n\n"
                    f"TEXT2:\n{example_text2}\n\n"
                    "OUTPUT:\n"
                    "{\n"
                    "  \"knowledge_graph1\": [\n"
                    "      [\"ISIS\", \"released\", \"more than 200 Yazidis\"],\n"
                    "      [\"Yazidis\", \"are\", \"minority group\"],\n"
                    "      [\"ISIS\", \"released\", \"women and elderly Yazidis\"],\n"
                    "      [\"Peshmerga commander\", \"said\", \"freed Yazidis are released\"]\n"
                    "  ],\n"
                    "  \"knowledge_graph2\": [\n"
                    "      [\"ISIS\", \"released\", \"more than 200 Yazidis\"],\n"
                    "      [\"Yazidis\", \"killed and displaced by\", \"ISIS\"],\n"
                    "      [\"ISIS\", \"released\", \"women and elderly Yazidis\"],\n"
                    "      [\"Yazidis\", \"are\", \"minority group\"],\n"
                    "      [\"Yazidis\", \"are of\", \"Kurdish descent\"],\n"
                    "      [\"Peshmerga commander\", \"said\", \"freed Yazidis are released\"]\n"
                    "      [\"Peshmerga\", \"received\", \"freed Yazidis\"],\n"
                    "      [\"Peshmerga\", \"sent\", \"freed Yazidis to Irbil\"],\n"
                    "      [\"ISIS\", \"conquered\", \"Sinjar\"],\n"
                    "      [\"ISIS\", \"caused\", \"humanitarian crisis\"],\n"
                    "      [\"Coalition\", \"responded with\", \"airdrops\"]\n"
                    "      [\"Coalition\", \"responded with\", \"rescues\"]\n"
                    "      [\"Coalition\", \"responded with\", \"airstrikes\"]\n"
                    "      [\"Arab tribal leaders\", \"helped coordinate\", \"release of Yazidis\"],\n"
                    "      [\"ISIS\", \"slaughtered\", \"Yazidis\"],\n"
                    "      [\"ISIS\", \"raped and enslaved\", \"female Yazidi captives\"],\n"
                    "      [\"Yazidis\", \"are followers of\", \"pre-Islamic religion\"],\n"
                    "      [\"Yazidis' religion\", \"draws from\", \"Christianity\"],\n"
                    "      [\"Yazidis' religion\", \"draws from\", \"Judaism\"],\n"
                    "      [\"Yazidis' religion\", \"draws from\", \"Zoroastrianism\"],\n"
                    "      [\"U.S. and other nations\", \"conducted\", \"airstrikes against ISIS\"],\n"
                    "      [\"Yazidis\", \"live in\", \"northern Iraq\"],\n"
                    "      [\"500,000 Yazidis\", \"live in\", \"northern Iraq\"]\n"
                    "  ]\n"
                    "}\n"
                )
            },
            {
                "role": "user",
                "content": f"TEXT1:\n{text1}\n\nTEXT2:\n{text2}"
            },
        ],
        temperature=0,
    )
    kg = response.choices[0].message.content
    return kg

# text1 = "brazilian coach ze maria was fired on wednesday after poor run . the romanian club have been sacked by ze maria for the second time . neamt neamt have been beaten by mid-table fc botosani on saturday . the former inter milan and parma right back in the bottom of the season . ze maria replaced the florin marin in january to become ceahlaul 's third coach ."
# text2 = "Relegation-threatened Romanian club Ceahlaul Piatra Neamt have sacked Brazilian coach Ze Maria for the second time in a week. Former Brazil defender Ze Maria was fired on Wednesday after a poor run, only to be reinstated the next day after flamboyant owner Angelo Massone decided to 'give the coaching staff another chance.' But the 41-year-old former Inter Milan and Parma right back, capped 25 times by Brazil, angered Massone again after Ceahlaul were beaten 2-0 by mid-table FC Botosani on Saturday. Ze Maria represented Brazil on 25 occasions during an international career spanning five years The result left Ceahlaul 16th in the standings, six points adrift of safety. Ze Maria replaced Florin Marin in January to become Ceahlaul's third coach this season. He will be replaced by Serbian Vanya Radinovic."
# generated = final_kg_constructor(text1, text2)
# KGs = json.loads(generated)
# claim_kg = KGs["knowledge_graph1"]
# context_kg = KGs["knowledge_graph2"]
# print(f"CLAIM:\n{claim_kg}\n\nCONTEXT:\n{context_kg}")

# text1 = "falcon 9 rocket carrying an uncrewed cargo spacecraft called dragon on a flight from cape canaveral . the two-stage two-stage falcon rocket landed on the drone ship in january . the rocket was the attempt to land a rocket stage on a floating barge for the first time . the company has said it will keep trying to land rocket on the ground ."
# text2 = "(CNN)SpaceX on Tuesday launched a two-stage Falcon 9 rocket carrying an uncrewed cargo spacecraft called Dragon on a flight from Cape Canaveral, Florida, to the International Space Station. That was the easy part. In a difficult bid to land a rocket stage on a floating barge for the first time, the private space exploration company was unsuccessful. SpaceX founder Elon Musk tweeted: \"Ascent successful. Dragon enroute to Space Station. Rocket landed on droneship, but too hard for survival.\" He later clarified that the rocket landed, but tipped over. SpaceX tried to land a Falcon 9 on the drone ship in January, but the rocket hit at an angle and exploded. SpaceX has said it will keep trying and, after it masters landing at sea, hopes to someday land rockets on the ground. Usually booster rockets burn up in Earth's atmosphere or, like NASA's space shuttle boosters, they fall back into the ocean. So why try to land one? Musk wants to cut costs. On his company's website, he says that if anyone can figure out how to \"reuse rockets just like airplanes, the cost of access to space will be reduced by as much as a factor of a hundred.\" What about the rest of the rocket and the Dragon? The smaller, top part of the rocket will carry the Dragon into orbit and then break away from the cargo ship and burn up in Earth's atmosphere. The Dragon will dock with the space station a couple of days after launch to deliver more than 4,300 pounds (1,950 kilograms) of supplies, including research equipment and ISSpresso, an espresso maker that astronauts can use to make coffee and tea. The space station crew will spend about five weeks unpacking the Dragon. They'll then stuff it with over 3,000 pounds of science experiments, trash and other stuff to send back to Earth. When they're done, Dragon will leave the space station and mission controllers will guide it to splashdown in the Pacific Ocean off California. This is the sixth SpaceX mission to the International Space Station. The company was the first private space contractor to dock with the station. Tuesday's launch was the second attempt for this mission. Monday's planned launch was scrubbed due to weather. CNN's Catherine E. Shoichet contributed to this report."
# generated = sandbox_kgs(text1, text2)
# print(generated)

# text1 = "tim durkan photographed aerial shots of the sunset warming the city 's skyline and shared them on cnn ireport . the fires were started in southeastern siberia , by farmers burning grass in their fields . the flames quickly grew out of control because of strong winds and spread throughout the region ."
# text2 = "(CNN)A fiery sunset greeted people in Washington Sunday. The deep reddish color caught Seattle native Tim Durkan's eye."# He photographed a handful of aerial shots of the sunset warming the city's skyline and shared them on CNN iReport. The stunning sunsets were the result of raging wildfires in parts of Siberia. \"The dramatic sunsets began showing up over the weekend and had Seattle locals wondering where the amber-colored haze was originating from,\" Durken said. The fires were started in southeastern Siberia, by farmers burning grass in their fields. But on April 14, it is believed that the flames quickly grew out of control because of strong winds and spread throughout the region, according to CNN affiliate KOMO-TV. As a result, the fires have destroyed dozens of villages in the region. Rescue crews were able to put out the flames. However, the lingering smoke from the widespread fires were picked up by atmospheric winds. The winds carried the smoke from Siberia across the Pacific Ocean and brought it to the Pacific Northwest. Parts of Oregon, Washington and British Columbia are seeing the results of the smoke, wind and solar light combination. The reason people are seeing an intense red sunset is a result of smoke particles filtering out the shorter wavelength colors from the sunlight like greens, blues, yellows and purples, KOMO-TV said. That means colors like red and orange are able to penetrate the air unfiltered. The colors are especially intense during sunrises and sunsets because there is more atmosphere for the light to travel through to get to a person's eye. As the smoke starts to dissipate, air quality will get better and these fiery sunsets will lose their reddish hue."
# generated = sandbox_kgs(text1, text2)
# print(generated)


def construct_kgs_just_text(text):
    """PROMPT INSPIRED BY https://arxiv.org/pdf/2407.10793"""
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are an expert at extracting information in structured formats to build a knowledge graph.\n"
             "Step 1 - Entity detection: Identify all entities in the raw text. Make sure not to miss any out. Entities should be basic and simple, they are akin to Wikipedia nodes.\n"
             "Step 2 - Coreference resolution: Find all expressions in the text that refer to the same entity. Make sure entities are not duplicated. In particular do not include entities that are more specific versions of themselves, e.g 'a detailed view of jupiter's atmosphere' and 'jupiter's atmosphere', only include the most specific version of the entity.\n"
             "Step 3 - Relation extraction: Identify semantic relationships between the entities you have identified.\n"
             "Format: Return the knowledge graph as a list of triples, i.e ['entity 1', 'relation 1-2', 'entity 2'], in Python code. Do not return anything in your output except for the python code. Do not provide any preamble or information about the input.\n"},
            {"role": "user", "content": f"Use the given format to extract information from the following inputs: <input>{text}</input>.\n"
             "Skip the preamble and output the result as a list <python></python> tags.\n"},
             {"role": "user", "content": f"Important Tips:\n"
              "1. Make sure all information is included in the knowledge graph \n"
              "2. Each triple must only contain three strings! None of the strings should be empty.\n"
              "3. Do not split up related information into separate triples because this could change the meaning.\n"
              "4. Make sure all brackets and quotation marks are matched.\n"
              "5. Before adding a triple to the knowledge graph, check the concatenated triple makes sense as a sentence. If not, discard it.\n"},
              {"role": "user", "content": f"Here are some example input and output pairs.\n\n"
               "## Example 1.\n"
               "Input:\n"
               "'The Walt Disney Company, commonly known as Disney, is an American multinational mass media and entertainment congolmerate that is headquartered at the Walt Disney Studios complex in Burbank, California.'\n"
               "Output:\n"
               "<python>\n"
               "[['The Walt Disney Company', 'headquartered at', 'Walt Disney Studious complex in Burbank, California'],\n"
               "['The Walt Disney Company', 'commonly known as', 'Disney'],\n"
               "['The Walt Disney Company', 'instance of', 'American multinational mass media and entertainment conglomerate']]\n"
               "</python>\n\n"
               "Example 2.\n"
               "Input:\n"
               "'John Russell Reynolds (1820–1876) was an English lawyer, judge, and author. He was born in London, the son of a barrister, and was educated at Eton College and Trinity College, Cambridge.'\n"
               "Output:\n"
               "<python>\n"
               "[['John Russell Reynolds', 'born', '1820'],\n"
               "['John Russell Reynolds', 'died', '1876'],\n"
               "['John Russell Reynolds', 'nationality', 'England'],\n"
               "['John Russell Reynolds', 'occupation', 'lawyer'],\n"
               "['John Russell Reynolds', 'occupation', 'judge'],\n"
               "['John Russell Reynolds', 'occupation', 'author'],\n"
               "['John Russell Reynolds', 'birthplace', 'London'],\n"
               "['John Russell Reynolds', 'father', 'barrister'],\n"
               "['John Russell Reynolds', 'educated at', 'Eton College'],\n"
               "['John Russell Reynolds', 'educated at', 'Trinity College']]\n"
               "</python>\n\n"
               "Example 3.\n"
               "Input:\n"
               "'Amanda Jackson was born in Springfield, Ohio, USA on June 1, 1985. She was a basketball player for the U.S women's team.'\n"
               "Output:\n"
               "<python>\n"
               "[['Amanda Jackson', 'born in', 'Springfield, Ohio, USA']\n"
               "['Amanda Jackson', 'born on', 'June 1, 1985']\n"
               "['Amanda Jackson', 'occupation', 'basketball player']\n"
               "['Amanda Jackson', 'played for', 'U.S women basketball team']]\n"
               "</python>"}
        ],
        temperature = 0
    )
    kg = response.choices[0].message.content

    return kg


def construct_kgs(text, sentences):
    """PROMPT INSPIRED BY https://arxiv.org/pdf/2407.10793"""
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are an expert at extracting information in structured formats to build a knowledge graph.\n"
             "Step 1 - Entity detection: Identify all entities in the raw text. Make sure not to miss any out. Entities should be basic and simple, they are akin to Wikipedia nodes.\n"
             "Step 2 - Coreference resolution: Find all expressions in the text that refer to the same entity. Make sure entities are not duplicated. In particular do not include entities that are more specific versions of themselves, e.g 'a detailed view of jupiter's atmosphere' and 'jupiter's atmosphere', only include the most specific version of the entity.\n"
             "Step 3 - Relation extraction: Identify semantic relationships between the entities you have identified.\n"
             "Format: Return the knowledge graph as a list of triples, i.e ['entity 1', 'relation 1-2', 'entity 2'], in Python code. Do not return anything in your output except for the python code. Do not provide any preamble or information about the input.\n"},
            {"role": "user", "content": f"Use the given format to extract information from the following inputs: <input>{text}</input>.\n"
             "Skip the preamble and output the result as a list within <python></python> tags.\n"},
             {"role": "user", "content": f"Important Tips:\n"
              "1. Make sure all information is included in the knowledge graph \n"
              "2. Each triple must only contain three strings! None of the strings should be empty.\n"
              "3. Do not split up related information into separate triples because this could change the meaning.\n"
              "4. Make sure all brackets and quotation marks are matched.\n"
              "5. Before adding a triple to the knowledge graph, check the concatenated triple makes sense as a sentence. If not, discard it.\n"},
              {"role": "user", "content": f"Here are some example input and output pairs\n\n"
               "## Example 1.\n"
               "Input:\n"
               "'The Walt Disney Company, commonly known as Disney, is an American multinational mass media and entertainment congolmerate that is headquartered at the Walt Disney Studios complex in Burbank, California.'\n"
               "Output:\n"
               "<python>\n"
               "[['The Walt Disney Company', 'headquartered at', 'Walt Disney Studious complex in Burbank, California'],\n"
               "['The Walt Disney Company', 'commonly known as', 'Disney'],\n"
               "['The Walt Disney Company', 'instance of', 'American multinational mass media and entertainment conglomerate']]\n"
               "</python>\n\n"
               "Example 2.\n"
               "Input:\n"
               "'John Russell Reynolds (1820–1876) was an English lawyer, judge, and author. He was born in London, the son of a barrister, and was educated at Eton College and Trinity College, Cambridge.'\n"
               "Output:\n"
               "<python>\n"
               "[['John Russell Reynolds', 'born', '1820'],\n"
               "['John Russell Reynolds', 'died', '1876'],\n"
               "['John Russell Reynolds', 'nationality', 'England'],\n"
               "['John Russell Reynolds', 'occupation', 'lawyer'],\n"
               "['John Russell Reynolds', 'occupation', 'judge'],\n"
               "['John Russell Reynolds', 'occupation', 'author'],\n"
               "['John Russell Reynolds', 'birthplace', 'London'],\n"
               "['John Russell Reynolds', 'father', 'barrister'],\n"
               "['John Russell Reynolds', 'educated at', 'Eton College'],\n"
               "['John Russell Reynolds', 'educated at', 'Trinity College']]\n"
               "</python>\n\n"
               "Example 3.\n"
               "Input:\n"
               "'Amanda Jackson was born in Springfield, Ohio, USA on June 1, 1985. She was a basketball player for the U.S women's team.'\n"
               "Output:\n"
               "<python>\n"
               "[['Amanda Jackson', 'born in', 'Springfield, Ohio, USA']\n"
               "['Amanda Jackson', 'born on', 'June 1, 1985']\n"
               "['Amanda Jackson', 'occupation', 'basketball player']\n"
               "['Amanda Jackson', 'played for', 'U.S women basketball team']]\n"
               "</python>"}
        ],
        temperature = 0
    )
    context_map = response.choices[0].message.content

    # Step 2: Extract entities and relations sentence-by-sentence with context
    sentence_triples = []
    for sentence in sentences:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are an expert at extracting information in structured formats to build a knowledge graph."},
                {"role": "user", "content": f"Given the context triples:\n{context_map}\n\nExtract knowledge graph triples from this sentence:\n\n{sentence}\n\nReturn only the triples as a list of lists in Python format, without any explanations or preambles.\n"
                 "Additionally, ensure proper formatting of the triples such that each triple is in the form ['entity 1', 'relation', 'entity 2'], with proper usage of commas. Your raw output should be able to be converted into a python list using eval().\n"
                 "For example, the triple ['Jeanine Marie Riley', 'year', 1970'], should be first converted to ['Jeanine Marie Riley', 'year', '1970'], before being returned. Remember to not return anything other than the triples (i.e no preamble), as your output is being directly converted into a python list using eval()."}
            ],
            temperature=0
        )
        triples = response.choices[0].message.content
        sentence_triples.append(eval(triples))  # Convert text output to a Python list
    
    return sentence_triples

    
def fix_json_response(text):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages = [
        {
        "role": "system",
        "content": (
            "IMPORTANT: Do not include anything in your response apart from JSON, so that it can be properly parsed.\n"
            "I have an incomplete JSON response that needs to be properly formatted.\n"
            "The current response contains a lot of redundant entities and/or relations. I need your help to remove these duplicate or redundant entities/relations and ensure that the JSON is well-structured so that it can be parsed by python's json.loads() function.\n"
            "Here is the incomplete JSON response:\n"
            f"{text[:2000]}\n\n"
            "Please remove any redundant entries, ensure all relationships and entities are unique, and provide a properly formatted JSON response.\n"
            "Here is an example of a properly formatted JSON object for your reference:\n"
            "{\n"
            "  \"entities\": [\"Paris\", \"France\", \"Eiffel Tower\"],\n"
            "  \"relations\": [\n"
            "    [\"Paris\", \"is the capital of\", \"France\"],\n"
            "    [\"Eiffel Tower\", \"is located in\", \"Paris\"]\n"
            "  ],\n"
            "}\n"
            "Please do not include anything in your response apart from the JSON, do not include any comments or anything else that is not directly part of the JSON object.\n"
        )
        }
        ],
        temperature=0
    )
    content = response.choices[0].message.content
    try:
        parsed_response = json.loads(content)
        return parsed_response
    except json.JSONDecodeError as e:
        print("###FIX_JSON_RESPONSE()###")
        print("couldnt fix JSON")
        #print(f"Input: {text}")
        print(f"Error parsing JSON response: {e}")
        print(f"Content: {content}")
        return None

def claim_from_dataset(text, labels):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "IMPORTANT: Do not return anything except for valid JSON format, as your response will be parsed as a proper JSON object.\n"
             "Your task is to take a list of claims, and construct a knowledge graph that incorporates the context from other claims in the list.\n"
             "This knowledge graph should encapsulate the semantic and logical meaning of the list of claims perfectly.\n"
             "You will be given the list of claims in the form of a piece of text (delimited by ###).\n"
            "You need to extract entities from this text as well as relations between each entity.\n"
            "For each relation that you extract, please include the corresponding item of the list of claims that it came from in the form of a list, where the first element of the list is the number of the claim and the second element of the list is the relation triple itself. Do the exact same for the entities.\n"
            f"There should be {labels} items in the list of claims, so ensure that you include relations for each of the {labels} input items. For example, if there were 3 input items, then your output should contain relationships for item 1, item 2, and item 3.\n"
            "Entities can be anything that is a key part of the text. Examples are people, places, subjects, objects, food, etc.\n"
            "The relations that you choose have to encapsulate the context and meaning of the text perfectly (taking into account all of the claims in the text).\n"
            "As for how you represent these knowledge graphs, you need to return two lists (one for entities, one for relations).\n"
            "It is very important that each relation has 3 components only, e.g ['Apples', 'type of', 'fruit']. If needed, relations can be split up so that there are multiple relations each with 3 components.\n"
            "If an entity is long, make sure to summarise it as concisely as possible, or split it up into multiple relations.\n"
            "The tuples in the relations list should be of the form (subject, relation, object). Relations must have exactly three elements. You cannot have more or less than three elements in any relation.\n"
            "Please return your response in JSON format, and do not include anything except for the JSON. A small example is as follows:\n"
            "###['Albert Einstein (1879-1955) was a German-born theoretical physicist.', 'He is widely-known for developing the theory of releativity.', 'He also made important contributions to quantum mechanics']###\n\n"
                      "{\n"
                      "  \"entities\": [\"Albert Einstein\", \"theoretical physicist\", \"Germany\", \"theory of relativity\", \"quantum mechanics\", \"1879\", \"1955\"],\n"
                      "  \"relations\": [\n"
                      "    [1, [\"Albert Einstein\", \"born\", \"Germany\"]],\n"
                      "    [1, [\"Albert Einstein\", \"occupation\", \"theoretical physicist\"]],\n"
                      "    [2, [\"Albert Einstein\", \"known for\", \"theory of relativity\"]],\n"
                      "    [3, [\"Albert Einstein\", \"contributed to\", \"quantum mechanics\"]],\n"
                      "    [1, [\"Albert Einstein\", \"born\", \"1879\"]],\n"
                      "    [1, [\"Albert Einstein\", \"died\", \"1955\"]]\n"
                      "  ],\n"
                      "}\n"},
            {"role": "user", "content": f"###{text}###\n\n"}
        ],
        temperature = 0
    )
    content = response.choices[0].message.content
    try:
        parsed_response = json.loads(content)
        return parsed_response
    except json.JSONDecodeError as e:
        print("###CLAIM_FROM_DATASET()###")
        print(f"Error parsing JSON response: {e}")
        print(f"Content: {content}")
        return None
    

def claim_from_dataset_2(context, curr_claim):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "Your task is to create a knowledge graph based on a claim (delimited by $$$) using some context (delimited by ###) to improve the knowledge graph.\n"
             "You are only allowed to construct the knowledge graph about the claim (delimited by $$$), i.e don't include any relations about other parts of the context which aren't contained within the claim.\n"
             "You are also only allowed to use information contained in the context, and should not use any other external knowledge to make these knowledge graphs.\n"
             "To create the knowledge graph, you must extract entities and relations about the claim. Entities can be anything that is a key part of the text. Examples are people, places, subjects, objects, food, etc.\n"
             "The relations that you choose have to encapsulate the context and meaning of the claim perfectly (taking into account the context).\n"
            "As for how you represent these knowledge graphs, you need to return two lists (one for entities, one for relations).\n"
            "It is very important that each relation has 3 components only, e.g ['Apples', 'type of', 'fruit']. If needed, relations can be split up so that there are multiple relations each with 3 components.\n"
            "If an entity is long, make sure to summarise it as concisely as possible, or split it up into multiple relations.\n"
            "The tuples in the relations list should be of the form (subject, relation, object). Relations must have exactly three elements. You cannot have more or less than three elements in any relation.\n"
            "Please return your response in JSON format, and do not include anything except for the JSON. A couple examples are as follows:\n"
            "###Albert Einstein (1879-1955) was a German-born theoretical physicist. He is widely-known for developing the theory of relativity. He also made important contributions to quantum mechanics### $$$He is widely-known for developing the theory of relativity$$$\n\n"
                      "{\n"
                      "  \"entities\": [\"Albert Einstein\", \"theory of relativity\"],\n"
                      "  \"relations\": [\n"
                      "     [\"Albert Einstein\", \"known for\", \"theory of relativity\"],\n"
                      "     [\"Albert Einstein\", \"developed\", \"theory of relativity\"]"
                      "  ],\n"
                      "}\n\n\n"
            "###Thomas Clayton Wolfe (October 3, 1900 – September 15, 1938) was an American novelist of the early twentieth century. Wolfe wrote four lengthy novels, plus many short stories, dramatic works, and novellas. He is known for mixing highly original, poetic, rhapsodic, and impressionistic prose with autobiographical writing. His books, written and published from the 1920s to the 1940s, vividly reflect on American culture and the mores of that period. His first novel, Look Homeward, Angel (1929), was a success. Wolfe's other novels—Of Time and the River (1935), The Web and the Rock (1939), and You Can't Go Home Again (1940)—were less successful but remain highly regarded. He is considered a major American modernist writer.### $$$Thomas Clayton Wolfe (October 3, 1900 – September 15, 1938) was an American novelist of the early twentieth century.$$$\n\n"
                      "{\n"
                      "  \"entities\": [\"Thomas Clayton Wolfe\", \"October 3, 1900\", \"September 15, 1938\", \"American novelist\", \"early twentieth century\"],\n"
                      "  \"relations\": [\n"
                      "     [\"Thomas Clayton Wolfe\", \"born\", \"October 3, 1900\"],\n"
                      "     [\"Thomas Clayton Wolfe\", \"died\", \"September 15, 1938\"],\n"
                      "     [\"Thomas Clayton Wolfe\", \"occupation\", \"American novelist\"]\n"
                      "  ],\n"
                      "}\n"
                      },
            {"role": "user", "content": f"###{context}### $$${curr_claim}$$$\n\n"}
        ],
        temperature = 0
    )
    content = response.choices[0].message.content
    try:
        parsed_response = json.loads(content)
        return parsed_response
    except json.JSONDecodeError as e:
        print("###CLAIM_FROM_DATASET()###")
        print(f"Error parsing JSON response: {e}")
        print(f"Content: {content}")
        return None
    
def filter_claims(text, claim):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "Your task is to filter claims (delimited by $$$) so that there are only claims relevant to the text (delimited by ###). Please return the claims in the same format (JSON) as they came, with no other output other than the claims\n"
             "Some of the entities in the text may have been filled in with more information (e.g he may have been turned into Albert Einstein, for example). This is ok, but having relations in the claim that are not at all part of the text should be removed.\n"
             "For example: see the following:\n\n"
             "Input: $$$[[\"Albert Einstein\", \"occupation\", \"theoretical physicist\"], [\"Albert Einstein\", \"developed\", \"theory of relativity\"], [\"Albert Einstein\", \"birthplace\", \"Germany\"]]$$$ ###Albert Einstein was a theoretical physicist who developed the theory of relativity###}\n"
             "Your response: [[\"Albert Einstein\", \"occupation\", \"theoretical physicist\"], [\"Albert Einstein\", \"developed\", \"theory of relativity\"]]\n\n"},
            {"role": "user", "content": f"$$${claim}$$$ ###{text}###\n\n"}
        ],
        temperature = 0
    )
    content = response.choices[0].message.content
    return content
    try:
        parsed_response = json.loads(content)
        return parsed_response
    except json.JSONDecodeError as e:
        print("###CLAIM_FROM_DATASET()###")
        print(f"Error parsing JSON response: {e}")
        print(f"Content: {content}")
        return None



# def extract_relevant_relations(list_of_relations, relation):
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You will receive a list of relations (denoted by ###).\n"
#         "Your task is to determine which relations are the most relevant to the relation denoted by ***.\n"
#         "Ensure that your chosen relations from the list of relations are as semantically similar as possible to the given relation. It is important that\n"
#         "you are confident about the semantic similarity, otherwise do not include it.\n"
#         "Please return your output in the form of a Python list.\n"
#         "If you cannot be confident that any of the relations in the list of relations are related to the relation, then just leave the list empty.\n"
#         "It is extremely important that your chosen relations are actually present in the list of relations (denoted by ###).\n"
#         "See below for examples:\n"
#         "list of relations: ### ['authority', 'maximum number of players', 'Great Russian Encyclopedia Online ID (old version)', 'industry'] ###, relation: *** 'player count' ***\n"
#         "output: ['maximum number of players']\n\n"
#         "list of relations: ### ['instance of', 'different from', 'subclass of', 'color', 'Giant Bomb ID', 'water footprint'] ###, relation: *** 'type of' ***\n"
#         "output: ['instance of', 'subclass of']\n\n"
#         "list of relations: ### ['Q2736', 'association football', 'country of origin', 'inception', 'regulated by', 'sport'] ###, relation: *** 'originates in' ***\n"
#         "output: ['country of origin']\n\n"
#         "list of relations: ### ['Q2736', 'association football', 'practiced by', 'sport', 'association football player'] ###, relation: *** 'practiced by' ***\n"
#         "output: ['practiced by']\n\n"},
#             {"role": "user", "content": f"list of relations: ### {list_of_relations} ###, relation: *** {relation} ***\n\noutput: "}
#         ],
#         temperature=0.2
#     )
#     content = response.choices[0].message.content
#     return content

def extract_relevant_relations(list_of_relations, relation):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You will receive a list of relations (denoted by ###).\n"
            "Your task is to determine which relation(s) in the list of relations is the most relevant to the relation denoted by ***.\n"
            "Ensure that your chosen relation from the list of relations is as semantically similar as possible to the given relation. It is important that\n"
            "you are confident about the semantic similarity, otherwise do not include it.\n"
            "Please return your output in the form of a Python list.\n"
            "If you cannot be confident that any of the relations in the list of relations are related to the relation, then just leave the list empty.\n"
            "It is extremely important that your chosen relation is actually present in the list of relations (denoted by ###).\n"
            "Do not include anything except for the desired output.\n"
            "Lastly, try to stick to the relation given, i.e., don't stretch it too far.\n"
            "When considering relevance, think about direct semantic matches or very close matches in meaning. Avoid relations that only have a vague or indirect connection.\n"
            "See below for examples:\n"
            "list of relations: ### ['authority', 'maximum number of players', 'Great Russian Encyclopedia Online ID (old version)', 'industry'] ###, relation: *** 'player count' ***\n"
            "output: ['maximum number of players']\n\n"
            "list of relations: ### ['instance of', 'different from', 'subclass of', 'color', 'Giant Bomb ID', 'water footprint'] ###, relation: *** 'type of' ***\n"
            "output: ['instance of']\n\n"
            "list of relations: ### ['Q2736', 'association football', 'country of origin', 'inception', 'regulated by', 'sport'] ###, relation: *** 'from' ***\n"
            "output: ['country of origin']\n\n"
            "list of relations: ### ['Q2736', 'association football', 'practiced by', 'sport', 'association football player'] ###, relation: *** 'practiced by' ***\n"
            "output: ['practiced by']\n\n"
            "list of relations: ### ['field of work', 'native language', 'occupation', 'employer', 'signature', 'place of burial', 'movement', 'genre', 'religion or worldview', 'image', 'place of birth', 'place of death', 'sex or gender', 'ISNI', 'VIAF ID', 'father', 'GND ID', 'Library of Congress authority ID', 'Union List of Artist Names ID', 'mother', 'country of citizenship', 'instance of', 'educated at', 'coat of arms image', 'National Library of Romania ID', 'Enciclopedia di Roma person ID', 'Portuguese National Library author ID', 'Nationale Thesaurus voor Auteursnamen ID', 'Tabakalera ID', 'Academy of Athens authority ID', 'NORAF ID', 'Vatican Library ID (former scheme)', 'National Library of Ireland ID', 'Lur Encyclopedic Dictionary ID', 'Google Arts & Culture entity ID', 'ScienceDirect topic ID', 'NCL ID', 'symogih.org ID', 'medical condition', 'ICCROM authority ID', 'IxTheo authority ID', 'Encyclopedia of China (Third Edition) ID', 'student of', 'Personality Database profile ID', 'Radio France person ID', 'WorldCat Entities ID', 'Teresianum authority ID', 'Met Constituent ID', 'The Encyclopedia of Fantasy ID', 'Süddeutsche Zeitung topic ID', 'Rai Teche person ID', 'Municipal Library of Trikala ID', 'MMB ID', 'Central Library of Volos authority ID', 'Levadia Library ID', 'Piraeus Bank Group Cultural Foundation Library (A) ID', 'Famous Birthdays ID', 'DFK Paris person ID', 'KBR person ID', 'Trismegistos author ID', 'Kunstindeks Danmark Artist ID', 'CiNii Research ID', 'Regensburg Classification', 'Oroklini Library ID', 'University of Barcelona authority ID', 'Rodovid ID', 'The Literary Encyclopedia person ID', 'manner of death', 'J. Paul Getty Museum agent ID', 'NUKAT ID', 'WikiKids ID', 'Kinobox person ID', 'NLC authorities', 'U.S. National Archives Identifier', 'Internet Speculative Fiction Database author ID', 'Gran Enciclopèdia Catalana ID', 'Parsifal cluster ID', 'KulturNav-ID', 'PMB – Personen der Moderne Basis person ID', 'Oxford Reference overview ID', 'museum-digital person ID', 'Swedish Open Cultural Heritage URI', 'Hanslick Online person ID', 'NNDB people ID', 'CANTIC ID (former scheme)', 'Korrespondenzen der Frühromantik person ID', 'CONOR.SI ID', 'Vikidia article ID', 'Gran Enciclopèdia Catalana ID (former scheme)', 'depicted by', 'EGAXA ID', 'NLA Trove people ID', 'described by source', 'Art UK artist ID', 'National Library of Latvia ID', 'NSK ID', 'languages spoken, written or signed', 'Encyclopædia Britannica Online ID', 'Sandrart.net person ID', \"topic's main template\", 'image of grave', 'Commons Creator page', 'birth name', 'zbMATH author ID', 'name in native language', 'MacTutor biography ID', 'Enciclopedia de la Literatura en México ID', 'lifestyle', 'University of Barcelona authority ID (former scheme)', 'BBC Things ID', 'Canadiana Authorities ID (former scheme)', 'NLP ID (old)', 'British Museum person or institution ID', 'GTAA ID', 'National Portrait Gallery (London) person ID', 'genealogics.org person ID', 'CERL Thesaurus ID', 'Web Gallery of Art ID', 'different from', 'CCAB ID', 'LibriVox author ID', 'Project Gutenberg author ID', 'Discogs artist ID', 'Les Archives du spectacle person ID', \"Treccani's Biographical Dictionary of Italian People ID\", 'work period (end)', 'National Gallery of Victoria artist ID', 'Artsy artist ID', 'FAST ID', 'Museum of Modern Art artist ID', 'BiblioNet author ID', 'Vegetti Catalog of Fantastic Literature NILF ID', 'National Gallery of Art artist ID', 'AGORHA person/institution ID', 'Stuttgart Database of Scientific Illustrators ID', 'Academic Tree ID', 'Structurae person ID', 'J. Paul Getty Museum agent DOR ID (old)', 'Nationalmuseum Sweden ID', 'name', 'Geni.com profile ID', 'BookBrainz author ID', 'Bibliothèque nationale de France ID', 'IdRef ID', 'CALIS ID', 'NACSIS-CAT author ID', 'Persée author ID', 'Unz Review author ID', 'BVMC person ID', 'Benezit ID', 'Shakeosphere person ID', 'FamilySearch person ID', 'Great Russian Encyclopedia Online ID (old version)', 'WikiTree person ID', 'permanent duplicated item', 'LBT person ID', 'UK National Archives ID', 'RERO ID (obsolete)', 'Runeberg author ID', 'Encyclopædia Universalis ID', 'NE.se ID', 'Catholic Encyclopedia ID', 'BAnQ authority ID', 'National Library of Greece ID', 'Treccani ID', 'Auckland Art Gallery artist ID', 'Quora topic ID', 'SNAC ARK ID', 'IMDb ID', 'NDL Authority ID', 'Te Papa agent ID', 'Cultureel Woordenboek ID', 'Minneapolis Institute of Art constituent ID', 'Babelio author ID', 'Commons category', 'openMLOL author ID', 'Artnet artist ID', 'BNMM authority ID', 'Art Renewal Center artist ID', 'DBC author ID', 'Open Library subject ID', 'Boijmans artist ID', 'SBN author ID', 'Bridgeman artist ID', 'SHARE Catalogue author ID', 'Semantic Scholar author ID', 'Pinakothek artist ID', 'Libraries Australia ID', 'Athenaeum person ID', 'YCBA agent ID', \"Christie's creator ID\", \"Treccani's Enciclopedia Italiana ID\", 'MusicBrainz artist ID', 'Store norske leksikon ID', 'gravsted.dk ID', 'Science Museum people ID', 'Itaú Cultural ID', 'Google Doodle', 'AKL Online artist ID', 'Isidore scholar ID', 'RA Collections ID', 'Städel Museum artist ID', 'said to be the same as', 'National Library Board Singapore ID', 'Piccio person ID', 'DEN Store Danske ID', 'Cesky hudebni slovnik osob a instituci ID', 'Brahms Online person ID', 'Smithsonian American Art Museum person ID', 'New General Catalog of Old Books and Authors ID', 'AllMusic artist ID', 'Uffizi artist ID', 'Glasklar ID', 'Oxford Biography Index Number', 'Panthéon de la Guerre ID', 'Picasso ID', 'Constitutional Court of Italy ID', 'Istituto centrale per il catalogo unico ID', 'Hungarian National Museum ID', 'Swiss National Library ID', 'Alpine Club UK ID', 'ONC authority ID', 'Italian National Agency for Higher Education and Research ID', 'Grove Art Online ID', 'Künstlerhaus person ID', 'Biographical Dictionary of American Economists ID', 'IMDb name ID', 'Palabra Virtual author ID', 'Bookogs author ID', 'Florentine Museum History of Science ID', 'Brockhaus Enzyklopädie ID', 'Autonomous University of Barcelona authority ID', 'Australian Music Centre artist ID', 'CSIC authority ID', 'AAAUTH ID', 'Alkmaar Digital Library ID', 'Kinopoisk person ID', 'BPN person ID', 'National Portrait Gallery (London) person ID (old)', 'Joconde person ID', 'Find a Grave burial memorial ID', 'IDAE Authority ID', 'Discogs artist ID (old)', 'Parliamentary Archives ID', 'Open Library author ID', 'Museum of Contemporary Art Tokyo artist ID', 'MFA Boston artist ID', 'Te Papa artist ID', 'SUDOC authorities ID', 'Open Library author ID (old)', 'LibriVox author ID (old)', 'Parliamentary Archives ID (old)', 'Find a Grave burial memorial ID (old)', 'Museu Picasso artist ID', 'Thesaurus Musicarum Latinarum author ID', 'Museum of Modern Art (MoMA) artist ID', 'Protagonists person ID', 'International Standard Name Identifier', 'Munzinger IBA ID', 'Munzinger Verlag ID', 'KRAL ID', 'MusicBrainz artist ID (old)', 'Art Institute of Chicago artist ID', 'History of Science Museum ID', 'Istituto centrale per il catalogo unico ID (old)', 'Norwegian National Library ID', 'Alumni Cantabrigienses ID', 'Estonian Biographical Center ID', 'UPV Authority ID', 'Munzinger IBA ID (old)', 'LAC Bibliography ID', 'Picasso ID (old)', 'Munzinger Verlag ID (old)', 'International Standard Name Identifier (old)', 'Discogs artist ID (older)', 'MusicBrainz artist ID (older)', 'Art Institute of Chicago artist ID (older)', 'History of Science Museum ID (old)', 'Istituto centrale per il catalogo unico ID (older)', 'Norwegian National Library ID (older)', 'Alumni Cantabrigienses ID (old)', 'Estonian Biographical Center ID (old)', 'UPV Authority ID (old)', 'Munzinger IBA ID (old old)', 'LAC Bibliography ID (old)', 'Munzinger Verlag ID (old old)', 'International Standard Name Identifier (old old)', 'discogs artist ID', 'artsy artist ID', 'encyclopædia britannica online ID', 'Grove Music Online ID', 'Grove Art Online artist ID', 'J. Paul Getty Museum artist ID', 'German National Library authority ID', 'Library of Congress authority ID (old)', 'NLA Trove ID', 'Gran Enciclopèdia Catalana ID', 'Treccani ID', 'Auckland Art Gallery artist ID', 'Google Doodle ID', 'J. Paul Getty Museum artist DOR ID', 'National Gallery of Art artist ID', 'Museu Picasso ID', 'Art UK artist ID', 'National Gallery of Victoria artist ID', 'Art Institute of Chicago artist ID', 'Museum of Modern Art artist ID', 'Museum of Contemporary Art Tokyo artist ID', 'International Standard Name Identifier', 'Artcyclopedia ID', 'VIAF ID'] ###, relation: *** 'speaks' ***\n"
            "output: ['native language'']"},
            {"role": "user", "content": f"list of relations: ### {list_of_relations} ###, relation: *** {relation} ***"}
        ],
        temperature=0
    )
    content = response.choices[0].message.content
    return content

def construct_kg_wikidata(entities, text):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "IMPORTANT: Do not return anything except for valid JSON format, as your response will be parsed as a proper JSON object.\n"
                      "Your task is to create knowledge graphs based on some text.\n"
                      "You will be given a list of detected entities (delimited by ###), and a piece of text (delimited by ***).\n"
                      "The list of detected entities will be a list of lists, where the first element of each list is its id code, and the second element is it's name.\n"
                      "The list of detected entities have been extracted from the text already.\n"
                      "You need to extract relations between entities from this text.\n"
                      "These relations should be summed up briefly, i.e try to shorten them down if they are long to a couple words.\n"
                      "Try to phrase the relations in a way similar to wikidata statements, e.g instead of using the word 'was', use 'occupation', if the context is about the job a person did in the text.\n"
                      "While doing this, keep in mind the context of that entity within the text, and how the entities within the text relate to each other.\n"
                      "The entities may not exactly match their counterpart in the text, i.e they may have slightly different spelling or phrasing, but should be treated the same.\n"
                      "If an entity does not have any relations to other entities within the text, that is ok.\n"
                      "The relations that you choose have to encapsulate the context and meaning of the text perfectly.\n"
                      "As for your response, you need to return a list of lists, where each list has three elements of form [subject, relation, object].\n"
                      "These relations must have exactly three elements. You cannot have more or less than three elements in any relation.\n"
                      "Do not include anything except for the desired output.\n"
                      "Please return your response in JSON format. For example, see the following:\n"
                      "###[('Q527', 'sky'), ('Q1088', 'blue'), ('Q197', 'plane'), ('Q765633', 'flying')]### ***The sky is blue, planes are flying in the sky***\n\n"
                      "{\n"
                      "  \"relations\": [\n"
                      "    [[\"Q527\", \"sky\"], \"color\", [\"Q1088\", \"blue\"]],\n"
                      "    [[\"Q197\", \"plane\"], \"flying in\", [\"Q527\", \"sky\"]]\n"
                      "  ],\n"
                      "}\n\n"
                      "###[('Q762', 'Leonardo da Vinci'), ('Q39631', 'physician'), ('Q12418', 'Mona Lisa')]### ***Leonardo da Vinci was a doctor who painted the Mona Lisa***\n\n"
                      "{\n"
                      "  \"relations\": [\n"
                      "    [[\"Q762\", \"Leonardo da Vinci\"], \"occupation\", [\"Q39631\", \"physician\"]],\n"
                      "    [[\"Q762\", \"Leonardo da Vinci\"], \"painted\", [\"Q12418\", \"Mona Lisa\"]]\n"
                      "  ],\n"
                      "}\n"},
            {"role": "user", "content": f"###{entities}### ***{text}***"}
        ],
        temperature=0
    )
    content = response.choices[0].message.content
    try:
        parsed_response = json.loads(content)
        return parsed_response
    except json.JSONDecodeError as e:
        print("###CONSTRUCT_KG_WIKIDATA()###")
        print(f"Error parsing JSON response: {e}")
        print(f"Content: {content}")
        return None
    

import json

def explain_ged_operations(claim_graph, evidence_graph, raw_explanations):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "Your task is to provide a user-friendly explanation based on the provided graphs and raw explanations.\n"
                      "You will be given two graphs: 'claim_graph' and 'evidence_graph', and a list of raw explanations detailing the discrepancies between them.\n"
                      "You need to generate a coherent and easily understandable explanation that summarises why the graphs are different based on these raw explanations and graphs.\n"
                      "Utilise context from the graphs and the raw explanations to provide a comprehensive overview.\n"
                      "Consider the following:\n"
                      "1. Highlight key differences between the claim and evidence graphs, including missing and additional nodes and relationships.\n"
                      "2. Explain why these differences matter and how they affect the accuracy or completeness of the claim or evidence.\n"
                      "3. Suggest possible reasons for the discrepancies, such as missing information or additional context in the evidence.\n"
                      "4. Ensure that the explanation is clear and accessible to users who may not be familiar with graph theory.\n"
                      "Return your response in a clear, structured format, similar to the provided example.\n"
                      "For example:\n"
                      "###Claim Graph###\n"
                      "Nodes: [Marie Curie, Radium, Nobel Prize in Physics, Nobel Prize in Chemistry]\n"
                      "Edges: [(Marie Curie, Radium, discovered), (Marie Curie, Nobel Prize in Physics, won), (Marie Curie, Nobel Prize in Chemistry, won)]\n"
                      "###Evidence Graph###\n"
                      "Nodes: [Albert Einstein, Radium, Grammy, Emmy]\n"
                      "Edges: [(Albert Einstein, Radium, found), (Marie Curie, Grammy, received), (Marie Curie, Emmy, was awarded)]\n"
                      "###Raw Explanations###\n"
                      "1. Nodes missing from the claim graph compared to the evidence graph:\n"
                      "- Grammy\n"
                      "- Emmy\n"
                      "2. Additional nodes in the evidence graph:\n"
                      "- Albert Einstein\n"
                      "3. Relationships present in the claim graph but missing in the evidence graph:\n"
                      "- (Marie Curie, Radium) with attributes {'relation': 'discovered'}\n"
                      "- (Marie Curie, Nobel Prize in Physics) with attributes {'relation': 'won'}\n"
                      "- (Marie Curie, Nobel Prize in Chemistry) with attributes {'relation': 'won'}\n"
                      "4. Relationships present in the evidence graph but missing in the claim graph:\n"
                      "- (Albert Einstein, Radium) with attributes {'relation': 'found'}\n"
                      "- (Marie Curie, Grammy) with attributes {'relation': 'received'}\n"
                      "- (Marie Curie, Emmy) with attributes {'relation': 'was awarded'}\n"
                      "###\n\n"
                      "Explanation:\n"
                      "The discrepancies between the claim and evidence graphs can be summarised as follows:\n"
                      "- The claim that Marie Curie discovered Radium could not be validated based on the evidence. Instead, the evidence suggests that Albert Einstein found Radium.\n"
                      "- The claim that Marie Curie won the Nobel Prize in Chemistry could not be validated based on the evidence, which instead shows that Marie Curie received the Grammy.\n"
                      "... and so on\n"
                    #   "1. **Missing Nodes:** The claim graph lacks nodes such as Grammy and Emmy, which are present in the evidence graph. This suggests that the claim may not cover all relevant aspects or achievements related to the entities involved.\n"
                    #   "2. **Additional Nodes:** The evidence graph includes additional nodes like Albert Einstein, which are not found in the claim graph. This indicates that the evidence contains information not captured in the claim.\n"
                    #   "3. **Incorrect Relationships:** The claim graph features relationships such as Marie Curie's discovery of Radium and her Nobel Prize wins, which are not supported by the evidence. This suggests potential inaccuracies or incomplete information in the claim.\n"
                    #   "4. **Additional Relationships:** The evidence graph shows relationships like Albert Einstein's discovery of Radium and Marie Curie's receipt of the Grammy and Emmy, which are missing in the claim. This indicates that the evidence provides additional context or updates that the claim does not reflect.\n"
                    #   "By addressing these discrepancies, you can align the claim more closely with the evidence, improving the accuracy and completeness of the information presented.\n"
                      "In your response, please only include the 'Explanation' part.\n"},
            {"role": "user", "content": f"###Claim Graph###\n{claim_graph} ###Evidence Graph###\n{evidence_graph}\n ###Raw Explanations###\n{raw_explanations}\n"}
        ],
        temperature=0
    )
    content = response.choices[0].message.content
    return content

    





# a = '[ "John Russell Reynolds (1820–1876) was an English lawyer, judge, and author.", "He was born in London, the son of a barrister, and was educated at Eton College and Trinity College, Cambridge.", "He was called to the bar in 1845, and became a Queens Counsel in 1859.", "He was appointed a judge of the Court of Common Pleas in 1867, and was knighted in 1871.", "Reynolds was a prolific author, writing on a wide range of topics.", "He wrote several books on legal topics, including The Law of Libel and Slander (1863), The Law of Copyright (1865), and The Law of Patents for Inventions (1868).", "He also wrote on a variety of other topics, including history, biography, and literature.", "He was a frequent contributor to the Saturday Review, and wrote several books on Shakespeare, including The Mystery of William Shakespeare (1848) and The Authorship of Shakespeare (1875).", "He also wrote a biography of the poet John Keats (1848)." ]'

# claim_entities = claim_from_dataset(a)['entities']
# claim_relations = claim_from_dataset(a)['relations']

# print(f"Entities: {claim_entities}")
# print(f"Relations: {claim_relations}")




# context = "John Russell Reynolds (1820–1876) was an English lawyer, judge, and author. He was born in London, the son of a barrister, and was educated at Eton College and Trinity College, Cambridge. He was called to the bar in 1845, and became a Queen's Counsel in 1859. He was appointed a judge of the Court of Common Pleas in 1867, and was knighted in 1871. Reynolds was a prolific author, writing on a wide range of topics. He wrote several books on legal topics, including The Law of Libel and Slander (1863), The Law of Copyright (1865), and The Law of Patents for Inventions (1868). He also wrote on a variety of other topics, including history, biography, and literature. He was a frequent contributor to the Saturday Review, and wrote several books on Shakespeare, including The Mystery of William Shakespeare (1848) and The Authorship of Shakespeare (1875). He also wrote a biography of the poet John Keats (1848)."
# claim = "He was born in London, the son of a barrister, and was educated at Eton College and Trinity College, Cambridge."
# print(claim_from_dataset_2(context, claim)['relations'])




def context_fill(sentences):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "Please output nothing except for JSON. Your task is to take a list of statements (denoted by ###), and create a knowledge graph for each statement.\n"
        "Knowledge graphs are defined as a list of triples, where each component of each triple is a string holding a single entity, e.g [[\"Apples\", \"type of\", \"fruit\"], [\"fruit\", \"is\", \"healthy\"]]\n"
        "Here is an un-related example of what you should do generally:\n\n"
        "###[\"Adiele Afigbo (1941–2006) was a Nigerian historian and professor of African history at the University of Nigeria, Nsukka.\", "
        "\"He was a pioneer in the field of African history and was known for his work on the history of the Igbo people of Nigeria.\", "
        "\"He was also a major contributor to the development of African historiography.\", "
        "\"Afigbo was born in 1941 in the town of Abiriba in Abia State, Nigeria.\", "
        "\"He attended the University of Ibadan, where he obtained a Bachelor of Arts degree in History in 1965.\", "
        "\"He then went on to pursue a Master of Arts degree in History at the University of London in 1967.\", "
        "\"He returned to Nigeria in 1968 and joined the faculty of the University of Nigeria, Nsukka, where he taught until his death in 2006.\", "
        "\"Afigbo was a prolific writer and researcher, and his works include The Warrant Chiefs: Indirect Rule in Southeastern Nigeria, 1891–1929 (1972), "
        "Ropes of Sand: Studies in Igbo History and Culture (1981), and The Abolition of the Slave Trade in S\"]###\n\n"
        "Example Knowledge Graphs:\n"
        "{{\n"
        "  \"Adiele Afigbo (1941–2006) was a Nigerian historian and professor of African history at the University of Nigeria, Nsukka.\" : [\n"
        "    [\"Adiele Afigbo\", \"birth year\", 1941],\n"
        "    [\"Adiele Afigbo\", \"death year\", 2006],\n"
        "    [\"Adiele Afigbo\", \"profession\", \"historian\"],\n"
        "    [\"Adiele Afigbo\", \"profession\", \"professor of African history\"],\n"
        "    [\"Adiele Afigbo\", \"institution\", \"University of Nigeria, Nsukka\"],\n"
        "    [\"Adiele Afigbo\", \"nationality\", \"Nigerian\"]\n"
        "  ],\n"
        "  \"He was a pioneer in the field of African history and was known for his work on the history of the Igbo people of Nigeria.\" : [\n"
        "    [\"Adiele Afigbo\", \"role\", \"pioneer in African history\"],\n"
        "    [\"Adiele Afigbo\", \"work focus\", \"history of the Igbo people of Nigeria\"]\n"
        "  ],\n"
        "  \"He was also a major contributor to the development of African historiography.\" : [\n"
        "    [\"Adiele Afigbo\", \"contribution\", \"development of African historiography\"]\n"
        "  ],\n"
        "  \"Afigbo was born in 1941 in the town of Abiriba in Abia State, Nigeria.\" : [\n"
        "    [\"Adiele Afigbo\", \"birth year\", 1941],\n"
        "    [\"Adiele Afigbo\", \"birthplace\", \"Abiriba\"],\n"
        "    [\"Adiele Afigbo\", \"birth state\", \"Abia State\"],\n"
        "    [\"Adiele Afigbo\", \"birth country\", \"Nigeria\"]\n"
        "  ],\n"
        "  \"He attended the University of Ibadan, where he obtained a Bachelor of Arts degree in History in 1965.\" : [\n"
        "    [\"Adiele Afigbo\", \"attended institution\", \"University of Ibadan\"],\n"
        "    [\"Adiele Afigbo\", \"degree obtained\", \"Bachelor of Arts in History\"],\n"
        "    [\"Adiele Afigbo\", \"degree year\", 1965]\n"
        "  ],\n"
        "  \"He then went on to pursue a Master of Arts degree in History at the University of London in 1967.\" : [\n"
        "    [\"Adiele Afigbo\", \"pursued degree\", \"Master of Arts in History\"],\n"
        "    [\"Adiele Afigbo\", \"degree institution\", \"University of London\"],\n"
        "    [\"Adiele Afigbo\", \"degree year\", 1967]\n"
        "  ],\n"
        "  \"He returned to Nigeria in 1968 and joined the faculty of the University of Nigeria, Nsukka, where he taught until his death in 2006.\" : [\n"
        "    [\"Adiele Afigbo\", \"returned to\", \"Nigeria\"],\n"
        "    [\"Adiele Afigbo\", \"joined faculty\", \"University of Nigeria, Nsukka\"],\n"
        "    [\"Adiele Afigbo\", \"teaching period\", \"1968–2006\"]\n"
        "  ],\n"
        "  \"Afigbo was a prolific writer and researcher, and his works include The Warrant Chiefs: Indirect Rule in Southeastern Nigeria, 1891–1929 (1972), Ropes of Sand: Studies in Igbo History and Culture (1981), and The Abolition of the Slave Trade in S\" : [\n"
        "    [\"Adiele Afigbo\", \"role\", \"prolific writer\"],\n"
        "    [\"Adiele Afigbo\", \"role\", \"researcher\"],\n"
        "    [\"Adiele Afigbo\", \"work\", \"The Warrant Chiefs: Indirect Rule in Southeastern Nigeria, 1891–1929\"],\n"
        "    [\"Adiele Afigbo\", \"work year\", 1972],\n"
        "    [\"Adiele Afigbo\", \"work\", \"Ropes of Sand: Studies in Igbo History and Culture\"],\n"
        "    [\"Adiele Afigbo\", \"work year\", 1981],\n"
        "    [\"Adiele Afigbo\", \"work\", \"The Abolition of the Slave Trade in S\"]\n"
        "  ]\n"
        "}}\n"
        "Please format the output as a JSON object where each statement maps to its corresponding list of triples.\n"},

        {"role": "user", "content": f"###{sentences}###\n\n"}
        ],
        temperature = 0
    )
    content = response.choices[0].message.content
    try:
        parsed_response = json.loads(content)
        return parsed_response
    except json.JSONDecodeError as e:
        print("###CLAIM_FROM_DATASET()###")
        print(f"Error parsing JSON response: {e}")
        print(f"Content: {content}")
        return None

    
    


# text = "Akila Dananjaya (born 2 August 1995) is a Sri Lankan cricketer. He made his international debut for the Sri Lankan cricket team in August 2018. He is a right-arm off-spinner and right-handed batsman. Dananjaya made his first-class debut for Sri Lanka Army Sports Club in the 2013–14 Premier League Tournament. He was the leading wicket-taker in the tournament, taking 32 wickets in seven matches."
# print(construct_kgs_just_text(text))



# sentences = str(["Adiele Afigbo (1941–2006) was a Nigerian historian and professor of African history at the University of Nigeria, Nsukka.", "He was a pioneer in the field of African history and was known for his work on the history of the Igbo people of Nigeria.", "He was also a major contributor to the development of African historiography.", "Afigbo was born in 1941 in the town of Abiriba in Abia State, Nigeria.", "He attended the University of Ibadan, where he obtained a Bachelor of Arts degree in History in 1965.", "He then went on to pursue a Master of Arts degree in History at the University of London in 1967.", "He returned to Nigeria in 1968 and joined the faculty of the University of Nigeria, Nsukka, where he taught until his death in 2006.", "Afigbo was a prolific writer and researcher, and his works include The Warrant Chiefs: Indirect Rule in Southeastern Nigeria, 1891–1929 (1972), Ropes of Sand: Studies in Igbo History and Culture (1981), and The Abolition of the Slave Trade in S"])
# print(context_fill(sentences))