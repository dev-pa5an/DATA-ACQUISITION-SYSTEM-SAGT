from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from asyncua import Client
import uvicorn

app = FastAPI()

# Serve static files (important for images, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure templates
templates = Jinja2Templates(directory="templates")


# OPC UA configuration (replace with your actual details)
opcua_url_17 = "opc.tcp://10.95.250.30:4840" #RT17
opcua_url_23 = "opc.tcp://10.95.250.123:4840" #RT23
opcua_url_33 = "opc.tcp://10.95.250.40:4840" #RT33
opcua_url_09 = "opc.tcp://10.101.187.80:4840" #RT09
opcua_url_34 = "opc.tcp://10.95.250.134:4840" #RT34
node_ids_09 = {
    "hoist": "ns=4;s=hoist_hours",
    "trolley": "ns=4;s=trolley_hours",
    "gantry": "ns=4;s=gantry_hours",
    "control_on": "ns=4;s=control_on_hours",
    "control_on_state": "ns=4;s=Master_control_relay",
    "soc1": "ns=4;s=soc_1",
    "soc2": "ns=4;s=soc_2",
    "soc3": "ns=4;s=soc_3"
    # ..4 any other nodes you need
}
node_ids_17 = {
    "hoist": "ns=4;s=hoist_hours",
    "trolley": "ns=4;s=trolley_hours",
    "gantry": "ns=4;s=gantry_hours",
    "control_on": "ns=4;s=control_on_hours",
    "control_on_state": "ns=4;s=Master_control_relay",
    "soc1": "ns=4;s=soc_1",
    "soc2": "ns=4;s=soc_2",
    "soc3": "ns=4;s=soc_3"
    # ... any other nodes you need
}
node_ids_33 = {
    "hoist": "ns=3;s=hoist_hours",
    "trolley": "ns=3;s=trolley_hours",
    "gantry": "ns=3;s=gantry_hours",
    "control_on": "ns=3;s=control_on_hours",
    "soc1": "ns=3;s=soc_1",
    "soc2": "ns=3;s=soc_2",
    "soc3": "ns=3;s=soc_3",
    "control_on_state": "ns=3;s=CTRLON"
    # ... any other nodes you need
}
node_ids_34 = {
    "hoist": "ns=3;s=hoist_hours",
    "trolley": "ns=3;s=trolley_hours",
    "gantry": "ns=3;s=gantry_hours",
    "control_on": "ns=3;s=control_on_hours",
    "soc1": "ns=3;s=soc_1",
    "soc2": "ns=3;s=soc_2",
    "soc3": "ns=3;s=soc_3",
    "control_on_state": "ns=3;s=CTRLON"
    # ... any other nodes you need
}
node_ids_23 = {
    "hoist": "ns=4;s=hoist_hours",
    "trolley": "ns=4;s=trolley_hours",
    "gantry": "ns=4;s=gantry_hours",
    "control_on": "ns=4;s=control_on_hours",
    "soc1": "ns=3;s=soc_1",
    "soc2": "ns=3;s=soc_2",
    "soc3": "ns=3;s=soc_3",
    "control_on_state": "ns=4;s=Master_control_relay"
    # ... any other nodes you need
}

async def get_node_value(opcua_url, node_id):  # Asynchronous function
    try:
        async with Client(url=opcua_url) as client:
            node = client.get_node(node_id)
            value = await node.read_value()
            return value
    except Exception as e: # Catching any exception during connection
        print(f"Error reading OPC UA node {node_id}: {e}")
        return None  # Or handle the error as needed

@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/get_hoist_hours_09")
async def read_hoist_hours_09():
    hoist_value = await get_node_value(opcua_url_09, node_ids_09["hoist"])
    trolley_value = await get_node_value(opcua_url_09, node_ids_09["trolley"])
    gantry_value = await get_node_value(opcua_url_09, node_ids_09["gantry"])
    control_on_value = await get_node_value(opcua_url_09, node_ids_09["control_on"])
    control_on_state = await get_node_value(opcua_url_09, node_ids_09["control_on_state"])
    soc1 = await get_node_value(opcua_url_09, node_ids_09["soc1"])
    soc2 = await get_node_value(opcua_url_09, node_ids_09["soc2"])
    soc3 = await get_node_value(opcua_url_09, node_ids_09["soc3"])

    return {
        "hoist_hours": (hoist_value + 7646.57 * 60) if hoist_value is not None else 17, # Return 0 if read fails
        "trolley_hours": (trolley_value + 5499.32 * 60) if trolley_value is not None else 17,
        "gantry_hours": (gantry_value + 2828.05 * 60) if gantry_value is not None else 17,
        "control_on_hours": control_on_value if control_on_value is not None else 17,
        "control_on_state": control_on_state if control_on_state is not None else 'false',
        "soc1": soc1 if soc1 is not None else '33f',
        "soc2": soc2 if soc2 is not None else '33f',
        "soc3": soc3 if soc3 is not None else '33f',
    }

@app.get("/get_hoist_hours_17")
async def read_hoist_hours_17():
    hoist_value = await get_node_value(opcua_url_17, node_ids_17["hoist"])
    trolley_value = await get_node_value(opcua_url_17, node_ids_17["trolley"])
    gantry_value = await get_node_value(opcua_url_17, node_ids_17["gantry"])
    control_on_value = await get_node_value(opcua_url_17, node_ids_17["control_on"])
    control_on_state = await get_node_value(opcua_url_17, node_ids_17["control_on_state"])
    soc1 = await get_node_value(opcua_url_17, node_ids_17["soc1"])
    soc2 = await get_node_value(opcua_url_17, node_ids_17["soc2"])
    soc3 = await get_node_value(opcua_url_17, node_ids_17["soc3"])

    return {
        "hoist_hours": (hoist_value + 9494.88 * 60) if hoist_value is not None else 17, # Return 0 if read fails
        "trolley_hours": (trolley_value + 4615.08 * 60) if trolley_value is not None else 17,
        "gantry_hours": (gantry_value + 2683.58* 60) if gantry_value is not None else 17,
        "control_on_hours": control_on_value if control_on_value is not None else 17,
        "control_on_state": control_on_state if control_on_state is not None else 'false',
        "soc1": soc1 if soc1 is not None else 57,
        "soc2": soc2 if soc2 is not None else 57,
        "soc3": soc3 if soc3 is not None else 57
    }
@app.get("/get_hoist_hours_33")
async def read_hoist_hours_33():
    hoist_value = await get_node_value(opcua_url_33, node_ids_33["hoist"])
    trolley_value = await get_node_value(opcua_url_33, node_ids_33["trolley"])
    gantry_value = await get_node_value(opcua_url_33, node_ids_33["gantry"])
    control_on_value = await get_node_value(opcua_url_33, node_ids_33["control_on"])
    soc1 = await get_node_value(opcua_url_33, node_ids_33["soc1"])
    soc2 = await get_node_value(opcua_url_33, node_ids_33["soc2"])
    soc3 = await get_node_value(opcua_url_33, node_ids_33["soc3"])
    control_on_state = await get_node_value(opcua_url_33, node_ids_33["control_on_state"])

    return {
        "hoist_hours": (hoist_value + 7380.85 * 60) if hoist_value is not None else '33f', # Return 0 if read fails
        "trolley_hours": (trolley_value + 3802.08 * 60) if trolley_value is not None else '33f',
        "gantry_hours": (gantry_value + 2059.87 * 60) if gantry_value is not None else '33f',
        "control_on_hours": control_on_value if control_on_value is not None else '33f',
        "soc1": soc1 if soc1 is not None else 63,
        "soc2": soc2 if soc2 is not None else 63,
        "soc3": soc3 if soc3 is not None else 63,
        "control_on_state": control_on_state if control_on_state is not None else 'true'
        
    }
@app.get("/get_hoist_hours_34")
async def read_hoist_hours_33():
    hoist_value = await get_node_value(opcua_url_34, node_ids_34["hoist"])
    trolley_value = await get_node_value(opcua_url_34, node_ids_34["trolley"])
    gantry_value = await get_node_value(opcua_url_34, node_ids_34["gantry"])
    control_on_value = await get_node_value(opcua_url_34, node_ids_34["control_on"])
    # soc1 = await get_node_value(opcua_url_34, node_ids_34["soc1"])
    # soc2 = await get_node_value(opcua_url_34, node_ids_34["soc2"])
    # soc3 = await get_node_value(opcua_url_34, node_ids_34["soc3"])
    control_on_state = await get_node_value(opcua_url_34, node_ids_34["control_on_state"])

    return {
        "hoist_hours": (hoist_value + 7685.02 * 60) if hoist_value is not None else '33f', # Return 0 if read fails
        "trolley_hours": (trolley_value + 3972.15 * 60) if trolley_value is not None else '33f',
        "gantry_hours": (gantry_value + 2140.3 * 60) if gantry_value is not None else '33f',
        "control_on_hours": (control_on_value + 434) if control_on_value is not None else '33f',
        # "soc1": soc1 if soc1 is not None else 63,
        # "soc2": soc2 if soc2 is not None else 63,
        # "soc3": soc3 if soc3 is not None else 63,
        "control_on_state": control_on_state if control_on_state is not None else 'true'
        
    }
@app.get("/get_hoist_hours_23")
async def read_hoist_hours_23():
    hoist_value = await get_node_value(opcua_url_23, node_ids_23["hoist"])
    trolley_value = await get_node_value(opcua_url_23, node_ids_23["trolley"])
    gantry_value = await get_node_value(opcua_url_23, node_ids_23["gantry"])
    control_on_value = await get_node_value(opcua_url_23, node_ids_23["control_on"])
    soc1 = await get_node_value(opcua_url_23, node_ids_23["soc1"])
    soc2 = await get_node_value(opcua_url_23, node_ids_23["soc2"])
    soc3 = await get_node_value(opcua_url_23, node_ids_23["soc3"])
    control_on_state = await get_node_value(opcua_url_23, node_ids_23["control_on_state"])

    return {
        "hoist_hours": hoist_value if hoist_value is not None else '33f', # Return 0 if read fails
        "trolley_hours": trolley_value if trolley_value is not None else '33f',
        "gantry_hours": gantry_value if gantry_value is not None else '33f',
        "control_on_hours": control_on_value if control_on_value is not None else '33f',
        "soc1": soc1 if soc1 is not None else 68,
        "soc2": soc2 if soc2 is not None else 68,
        "soc3": soc3 if soc3 is not None else 68,
        "control_on_state": control_on_state if control_on_state is not None else 'false'
        
    }

if __name__ == "__main__":
    # uvicorn.run(app, host="10.92.221.32", port=8000) # Listen on all interfaces
    uvicorn.run(app, host="10.92.221.32", port=8000) # Listen on all interfaces