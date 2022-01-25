from aiohttp import ClientSession, BasicAuth, ContentTypeError


class Response(dict):
    def __repr__(self):
        return '<RequestAsyncResponse: [' + str(self['status']) + ']'
    def json(self):
        return self['json']
    

async def request_async(method, *args, **kwargs):
    async with  ClientSession() as session:
        method = eval(f'session.{method}')
        async with method(*args, **kwargs) as response:
            dict_response={}
            for i in [i for i in dir(response) if not i.startswith('_')]:
                if not callable(eval('response.'+i)):
                    dict_response.update({i:eval('response.'+i)})
                elif i in ['get_encoding', 'json', 'release', 'text']:
                    print(i)
                    try:
                        r=eval('response.'+i+'()')
                        print(r)
                        r = r if not asyncio.iscoroutine(r) else await r
                    except ContentTypeError as e:
                        print(e)
                        r=e
                    
                    dict_response.update({i:r})
                    
            return Response(dict_response)
        
        
async def get(*args, **kwargs):
    return await request_async('get', *args, **kwargs)

async def post(*args, **kwargs):
    return await request_async('post', *args, **kwargs)

async def delete(*args, **kwargs):
    return await request_async('delete', *args, **kwargs)


import asyncio
async def create_tasks(*tasks):
    tasks = [asyncio.create_task(i) for i in tasks]
    l = asyncio.gather(*tasks)
    return l

async def run_async_tasks(*tasks):
    response = await create_tasks(*tasks)
    await response
    response = response.result()
    return response
   

