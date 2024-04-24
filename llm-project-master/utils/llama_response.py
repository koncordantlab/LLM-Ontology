from models.llama import get_llama_response

input = '''We are trying to figure out some causes of climate change and some impacts of it. We want to create a graph of relations bewteen these things. Interpret the text and generate an output using the following format and must only use relations from the specified list:

        Format:
        Entity1-relation-Entity2

        e.g. X-relation-Y
        
        Relations:
        causes
		impacts

        Context:

In common usage, climate change describes global warming—the ongoing increase in global average temperature—and its effects on Earth's climate system. Climate change in a broader sense also includes previous long-term changes to Earth's climate. The current rise in global average temperature is more rapid than previous changes, and is primarily caused by humans burning fossil fuels. Fossil fuel use, deforestation, and some agricultural and industrial practices add to greenhouse gases, notably carbon dioxide and methane.[4] Greenhouse gases absorb some of the heat that the Earth radiates after it warms from sunlight. Larger amounts of these gases trap more heat in Earth's lower atmosphere, causing global warming.

Climate change is causing a range of increasing impacts on the environment. Deserts are expanding, while heat waves and wildfires are becoming more common. Amplified warming in the Arctic has contributed to melting permafrost, glacial retreat and sea ice loss.'''

print(get_llama_response(input))