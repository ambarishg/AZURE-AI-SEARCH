from dotenv import load_dotenv,dotenv_values


load_dotenv()

# deployement_id with a model without a private end point 
values_env_openai = dotenv_values(".env2")

# deployement_id with a model with a private end point
#values_env_openai = dotenv_values(".env")

key = values_env_openai['KEY']
location = values_env_openai['LOCATION']
endpoint = values_env_openai['ENDPOINT']
deployment_id=values_env_openai['DEPLOYMENT_ID']  