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
opcua_url_17 = "opc.tcp://10.95.250.30:4840" # Update if needed #RT17
opcua_url_33 = "opc.tcp://10.95.250.40:4840" #RT33
node_ids_17 = {
    "hoist": "ns=4;s=hoist_hours",
    "trolley": "ns=4;s=trolley_hours",
    "gantry": "ns=4;s=gantry_hours",
    "control_on": "ns=4;s=control_on_hours",
    "control_on_state": "ns=4;s=XX_control_on"
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

@app.get("/get_hoist_hours_17")
async def read_hoist_hours_17():
    hoist_value = await get_node_value(opcua_url_17, node_ids_17["hoist"])
    trolley_value = await get_node_value(opcua_url_17, node_ids_17["trolley"])
    gantry_value = await get_node_value(opcua_url_17, node_ids_17["gantry"])
    control_on_value = await get_node_value(opcua_url_17, node_ids_17["control_on"])
    control_on_state = await get_node_value(opcua_url_17, node_ids_17["control_on_state"])

    return {
        "hoist_hours": hoist_value if hoist_value is not None else 17, # Return 0 if read fails
        "trolley_hours": trolley_value if trolley_value is not None else 17,
        "gantry_hours": gantry_value if gantry_value is not None else 17,
        "control_on_hours": control_on_value if control_on_value is not None else 17,
        "control_on_state": control_on_state if control_on_state is not None else 'false'
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
        "hoist_hours": hoist_value if hoist_value is not None else '33f', # Return 0 if read fails
        "trolley_hours": trolley_value if trolley_value is not None else '33f',
        "gantry_hours": gantry_value if gantry_value is not None else '33f',
        "control_on_hours": control_on_value if control_on_value is not None else '33f',
        "soc1": soc1 if soc1 is not None else '33f',
        "soc2": soc2 if soc2 is not None else '33f',
        "soc3": soc3 if soc3 is not None else '33f',
        "control_on_state": control_on_state if control_on_state is not None else 'false'
        
    }


if __name__ == "__main__":
    uvicorn.run(app, host="10.92.221.32", port=8000) # Listen on all interfaces