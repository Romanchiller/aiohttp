import asyncio

import aiohttp


async def main():
    client = aiohttp.ClientSession()
    #
    # response = await client.post(
    #     "http://127.0.0.1:8080/user",
    #     json={
    #         "name": "roman",
    #           "password": "Password2"
    #           },
    # )
    # print(response.status)
    # print(await response.json())
    #
    #
    # response = await client.post("http://127.0.0.1:8080/login",
    #                              json={'name': 'roman',
    #                                    'password': 'Password2'})
    # print(response.status)
    # print(await response.json())

    # response = await client.post(
    #     "http://127.0.0.1:8080/adv",
    #     json={"header": "zagolovok2122",
    #           # "description": "opisanie222",
    #           # 'sds': 'asdw'
    #           },
    #     # headers={'Authorization': '6e6451fe-b41d-45c3-897e-941f324697f0'},
    #     headers={'Authorization': '7b91044c-9cf4-4f4e-9bd1-0328a7b1b24f'},
    # )
    # print(response.status)
    # print(await response.json())



    # response = await client.get("http://127.0.0.1:8080/adv/1")
    # print(response.status)
    # print(await response.json())
    # #
    # response = await client.get("http://127.0.0.1:8080/adv/2")
    # print(response.status)
    # print(await response.json())

    response = await client.get("http://127.0.0.1:8080/user/1")
    print(response.status)
    print(await response.json())


    response = await client.patch("http://127.0.0.1:8080/user/1",
                                  # headers={'Authorization': 'cee6bb9a-c52d-4fa9-99c5-400516f9e388'},
                                  headers={'Authorization': 'cfeab4c6-8bde-4d34-b40d-3080458b3a34'},
                                  json={'name': 'new_header3'}
                                  )
    print(response.status)
    print(await response.json())

    # response = await client.delete("http://127.0.0.1:8080/adv/1",
    #                               # headers={'Authorization': 'cee6bb9a-c52d-4fa9-99c5-400516f9e388'},
    #                               headers={'Authorization': '7b91044c-9cf4-4f4e-9bd1-0328a7b1b24f'},
    #                               )
    # print(response.status)
    # print(await response.json())

    response = await client.get("http://127.0.0.1:8080/user/1")
    print(response.status)
    print(await response.json())
    #
    # response = await client.delete("http://127.0.0.1:8080/user/1",
    #                                # headers={'Authorization': 'f0daa6b9-a38c-4ddf-949c-16156d25fa95'},
    #                                headers={'Authorization': '93125424-eadc-4f3a-86fc-b3b692324ccf'},
    #                                )
    # print(response.status)
    # print(await response.json())
    #
    # response = await client.get("http://127.0.0.1:8080/user/1")
    # print(response.status)
    # print(await response.json())


    response = await client.post(
        "http://127.0.0.1:8080/adv",
        json={"header": "zagolovok12",
              "description": "opisanie1",
              'author_id': 1,
              'sadasda': 'asdasd'},
        headers={'Authorization': 'cfeab4c6-8bde-4d34-b40d-3080458b3a34'},
    )
    print(response.status)
    print(await response.json())
    #
    #
    response = await client.get("http://127.0.0.1:8080/adv/1")
    print(response.status)
    print(await response.json())
    #
    response = await client.patch("http://127.0.0.1:8080/adv/1",
                                  json={'header': 'noviy zagolovok'},
                                  headers={'Authorization': 'cfeab4c6-8bde-4d34-b40d-3080458b3a34'},
                                  )
    print(response.status)
    print(await response.json())


    response = await client.delete("http://127.0.0.1:8080/adv/1")
    print(response.status)
    print(await response.json())
    #
    # response = await client.get("http://127.0.0.1:8080/adv/1")
    # print(response.status)
    # print(await response.json())




    await client.close()


asyncio.run(main())
