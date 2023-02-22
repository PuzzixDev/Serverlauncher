import pypresence
import time

class presents:
    client_id = '1062914822452297790'
    rpc = pypresence.Presence(client_id)

    rpc.connect()

    rpc.update(state="server, maybe.", details="Creating a minecraft", large_image="large", small_image="small")

    time.sleep(100)

    rpc.close()