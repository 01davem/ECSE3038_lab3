from fastapi import FastAPI, HTTPException
import uuid

app = FastAPI()


tanks = []


@app.get('/tank', response_model=list)
def get_all_tanks():
    return tanks


@app.get('/tank/{tank_id}', response_model=dict)
def get_tank(tank_id: uuid.UUID):
    tank = next((t for t in tanks if t['id'] == tank_id), None)
    if tank:
        return tank
    else:
        raise HTTPException(status_code=404, detail="Tank not found")


@app.post('/tank', response_model=dict)
def create_tank(location: str, lat: float, long: float):
    new_tank = {
        "id": str(uuid.uuid4()),
        "location": location,
        "lat": lat,
        "long": long
    }
    tanks.append(new_tank)
    return new_tank


@app.patch('/tank/{tank_id}', response_model=dict)
def update_tank(tank_id: uuid.UUID, location: str, lat: float, long: float):
    tank = next((t for t in tanks if t['id'] == tank_id), None)
    if tank:
        tank['location'] = location
        tank['lat'] = lat
        tank['long'] = long
        return tank
    else:
        raise HTTPException(status_code=404, detail="Tank not found")


@app.delete('/tank/{tank_id}', status_code=204)
def delete_tank(tank_id: uuid.UUID):
    global tanks
    tanks = [t for t in tanks if t['id'] != tank_id]

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)
