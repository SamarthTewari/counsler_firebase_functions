
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.pydantic_v1 import BaseModel, Field
from action_verbs_storage import *
from helper_functions import *




class ExtracurricularActivityOutput(BaseModel):
    responsibility_one: str = Field(description="The first responsibility, mentioned as a single concise bullet point")
    responsibility_two: str = Field(description="The second responsibility, mentioned as a single concise bullet point")


# Create the HuggingFaceEndpoint LLM instance

output_parser = PydanticOutputParser(pydantic_object=ExtracurricularActivityOutput)

prompt_2_traits_with_topic_guidance = "I will give you a description of a extracurricular activity a highschool student preforms. " \
        "I would like you to return exactly two concise bullet points with a responsibility (not already described) they could have had while participating in that extracurricular activity." \
        "The first bullet point (50 characters) must be geared towards the {trait_one} of the student, must use one or more numerical measures, and use one of the following verbs: {verbs_trait_one}" \
        "The second bullet point (50 characters) must be geared towards the {trait_two} of the student, must use exactly one numerical measure, and must use one of the following verbs: {verbs_trait_two} " \
        "\n{format_instructions}\n" \
        "Description: {description}"



system = ("I will give you a description of a extracurricular activity a highschool student preforms. " \
        "I would like you to return exactly two concise bullet points with a responsibility (not already described) they could have had while participating in that extracurricular activity.")

human = ("Description: {description}\n"
        "Generate two concise bullet points (50 characters each) for responsibilities:\n"
        "1.The first bullet point (50 characters) must be geared towards the {trait_one} of the student, must use one or more numerical measures, and use one of the following verbs: {verbs_trait_one}" \
        "2. The second bullet point (50 characters) must be geared towards the {trait_two} of the student, must use exactly one numerical measure, and must use one of the following verbs: {verbs_trait_two}" \
        "Return each bullet point as a single string. Follow this format:\n{format_instructions}")

# Create the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("human", human)
])










'''hub_llm = HuggingFaceEndpoint(
    endpoint_url="https://ywcgr6ga3v6qgaq0.us-east-1.aws.endpoints.huggingface.cloud",
)
prompt = PromptTemplate(
    input_variables=["trait_one","trait_two","description","verbs_trait_one", "verbs_trait_two"],
    template=prompt_2_traits_with_topic_guidance,
    partial_variables={"format_instructions": output_parser.get_format_instructions()}
)
'''

def return_generated_extracurricular_description(description, trait_one, trait_two, verbs_not_to_use_trait_one, verbs_not_to_use_trait_two, temperature_setting):
    # TODO FIND HOW TO HIDE ENVIRONMENT VARIABLES!!

    groq_llm = ChatGroq(
    temperature= temperature_setting,
    model="llama3-70b-8192",
    api_key="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"
    )
    structured_llm = groq_llm.with_structured_output(ExtracurricularActivityOutput)

    trait_one_verbs = array_names_to_values_dict.get(trait_one)
    trait_two_verbs = array_names_to_values_dict.get(trait_two)
    
    suggested_verbs_for_trait_one = remove_random_elements(filter_verbs(action_verbs=trait_one_verbs, verbs_to_exclude=verbs_not_to_use_trait_one))
    suggested_verbs_for_trait_two = remove_random_elements(filter_verbs(action_verbs=trait_two_verbs, verbs_to_exclude=verbs_not_to_use_trait_two))

    joined_verbs1 = ", ".join(suggested_verbs_for_trait_one)
    joined_verbs2 = ", ".join(suggested_verbs_for_trait_two)



    input_data = {
        "description": description,
        "trait_one": trait_one,
        "trait_two": trait_two,
        "verbs_trait_one": joined_verbs1,
        "verbs_trait_two": joined_verbs2,
        "format_instructions": output_parser.get_format_instructions()
    }
    formatted_input = prompt.format(**input_data)


    #chain = prompt | groq_llm
    
    # Invoke the structured LLM
    result = structured_llm.invoke(formatted_input)

    
    
    # Process the result
    responsibility_one = result.responsibility_one
    responsibility_two = result.responsibility_two

    
    
    trait_one_verbs = array_names_to_values_dict.get(trait_one)
    trait_two_verbs = array_names_to_values_dict.get(trait_two)
    
    

    '''sequence = prompt | structured_llm | output_parser

    # Run the sequence and print the result
    #result = sequence.invoke({"trait_one": trait_one, "trait_two": trait_two, "description": description, "verbs_trait_one": joined_verbs1, "verbs_trait_two": joined_verbs2})'''

    cleaned_responsibility_one = replace_words_with_spaces_in_output(description=description, generated_llm_output=responsibility_one)
    cleaned_responsibility_two = replace_words_with_spaces_in_output(description=description, generated_llm_output=responsibility_two)
    

    if cleaned_responsibility_one[-1] not in '.?!':
        cleaned_responsibility_one = cleaned_responsibility_one + "."

    final_output = f"{cleaned_responsibility_one} {cleaned_responsibility_two}"

    return {"output": final_output}




