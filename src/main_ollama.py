
import json
import ollama
import asyncio

MODEL = "llama3.2"

# Simulates an API call to get flight times
# In a real application, this would fetch data from a live database or API
def get_flight_times(departure: str, arrival: str) -> str:
  print(f"Call out to get_flight_times function for: {departure}, {arrival}")

  flights = {
    'NYC-LAX': {'departure': '08:00 AM', 'arrival': '11:30 AM', 'duration': '5h 30m'},
    'LAX-NYC': {'departure': '02:00 PM', 'arrival': '10:30 PM', 'duration': '5h 30m'},
    'LHR-JFK': {'departure': '10:00 AM', 'arrival': '01:00 PM', 'duration': '8h 00m'},
    'JFK-LHR': {'departure': '09:00 PM', 'arrival': '09:00 AM', 'duration': '7h 00m'},
    'CDG-DXB': {'departure': '11:00 AM', 'arrival': '08:00 PM', 'duration': '6h 00m'},
    'DXB-CDG': {'departure': '03:00 AM', 'arrival': '07:30 AM', 'duration': '7h 30m'},
  }

  key = f'{departure}-{arrival}'.upper()
  return json.dumps(flights.get(key, {'error': 'Flight not found'}))

def get_calculation(calculation):
  print(f"Call out to get_calculation function for: {calculation}")
  try:
    calc = eval(calculation)
  except Exception as e:
    print(f"ERROR: eval failed with : {e}")

  return json.dumps({'result': calc})


async def run(model: str):
  client = ollama.AsyncClient()
  # Initialize conversation with a user query
  messages = [
    # {'role': 'user', 'content': 'What is the flight time from New York (NYC) to Los Angeles (LAX)?'},
    {'role': 'user', 'content': 'What is 64 times 10 and then divded by 2?'},
    # {'role': 'user', 'content': 'Act like an expert in gold trading and investments.  What are the basic in gold trading in the uK?'},
    ]

  # First API call: Send the query and function description to the model
  response = await client.chat(
    model=model,
    messages=messages,
    tools=[
      {
        'type': 'function',
        'function': {
          'name': 'get_flight_times',
          'description': 'Get the flight times between two cities',
          'parameters': {
            'type': 'object',
            'properties': {
              'departure': {
                'type': 'string',
                'description': 'The departure city (airport code)',
              },
              'arrival': {
                'type': 'string',
                'description': 'The arrival city (airport code)',
              },
            },
            'required': ['departure', 'arrival'],
          },
        },
      },

      {
        'type': 'function',
        'function': {
          'name': 'get_calculation',
          'description': 'Get the result of a numerical calculation',
          'parameters': {
            'type': 'object',
            'properties': {
              'calculation': {
                'type': 'string',
                'description': 'The calculation in a form that python can understand, e.g. (12 / 2) * 4.2',
              },
            },
            'required': ['calculation'],
          },
        },
      },    

    ],
  )

  # Add the model's response to the conversation history
  messages.append(response['message'])

  # Check if the model decided to use the provided function
  if not response['message'].get('tool_calls'):
    print("The model didn't use the function. Its response was:")
    print(response['message']['content'])
    return

  # Process function calls made by the model
  if response['message'].get('tool_calls'):
    for tool in response['message']['tool_calls']:

      function_response = None
      tool_name = tool['function']['name']

      if tool_name == 'get_flight_times':
        function_response = get_flight_times(tool['function']['arguments']['departure'], tool['function']['arguments']['arrival'])
      elif tool_name == 'get_calculation':
        function_response = get_calculation(tool['function']['arguments']['calculation'])

      # Add function response to the conversation
      messages.append(
        {
          'role': 'tool',
          'content': function_response,
        }
      )

  # Second API call: Get final response from the model
  final_response = await client.chat(model=model, messages=messages)
  print(final_response['message']['content'])


# Run the async function
asyncio.run(run(MODEL))