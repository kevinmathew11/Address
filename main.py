import models
import schemas
import uvicorn
import logging
import json
from fastapi import FastAPI, status, Depends, HTTPException, Response
from database import Base, engine
from sqlalchemy.orm import Session
from database import get_session
from typing import List
from haversine import haversine, Unit

# setup loggers
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)  # the __name__ resolve to "main" since we are at the root of the project.

# Create the database
Base.metadata.create_all(engine)

# Initialize app
app = FastAPI()


@app.get("/")
def root():
    return "Address Book"


@app.post("/address", response_model=schemas.AddressView, status_code=status.HTTP_201_CREATED)
def add_address(address: schemas.AddressCreate, session: Session = Depends(get_session)):
    """
    created_date: Optional[str]
    name: str
    city: str
    state: str
    pincode: int
    latitude: float
    longitude: float

    Example:
        {
          "name": "EastVantage",
          "city": "Bangalore",
          "state": "string",
          "latitude": 12.95176,
          "longitude": 77.60798
        }


    """
    address_db_entry = models.AddressEntry(name=address.name, city=address.city, state=address.state,
                                           latitude=address.latitude,
                                           longitude=address.longitude)
    logger.info("successfully validated input json")
    # add entry to the database
    session.add(address_db_entry)
    session.commit()
    session.refresh(address_db_entry)
    logger.info("successfully added entry to database")
    # return the addressBook object
    return address_db_entry


@app.get("/address", response_model=List[schemas.AddressView])
def fetch_all_address(session: Session = Depends(get_session)):
    # get all entries in address database
    addresses = session.query(models.AddressEntry).all()
    return addresses


@app.get("/address/{id}", response_model=schemas.AddressView)
def fetch_address(id: int, session: Session = Depends(get_session)):
    """
    Fetch address having the given id
    Args:
        id: id of the record
        session: database session

    Returns:

    """
    logger.info(f"Querying database for address with ID {id}")
    address = session.query(models.AddressEntry).get(id)
    if not address:
        msg = f"ID-{id} not found"
        logger.error(msg)
        raise HTTPException(status_code=404, detail=msg)
    return address


@app.put("/address/{id}", response_model=schemas.AddressView)
def update_address(id: int, address_update_request: schemas.AddressCreate,
                   session: Session = Depends(get_session)):
    # get the addressBook item with the given id
    address = session.query(models.AddressEntry).get(id)

    if address:
        address_update_request = json.loads(address_update_request.json())
        address.name = address_update_request["name"]
        address.city = address_update_request["city"]
        address.latitude = address_update_request["latitude"]
        address.longitude = address_update_request["longitude"]
        session.commit()
    else:
        msg = f"ID-{id} not found"
        logger.error(msg)
        raise HTTPException(status_code=404, detail=msg)
    return address


@app.delete("/address/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_addressBook(id: int, session: Session = Depends(get_session)):
    """

    Args:
        id: id of the entry to be deleted
        session: database session

    Returns:

    """
    # query if address with given id exists
    address = session.query(models.AddressEntry).get(id)
    # if address with given id exists,delete it from the database
    if address:
        session.delete(address)
        session.commit()
    else:
        msg = f"Found no address record with id {id}"
        logger.error(msg)
        raise HTTPException(status_code=404, detail=msg)
    msg = f"Deleted record with id {id}"
    return {"message": msg}


@app.get("/find_distance", response_model=List[schemas.AddressView])
def get_address_by_coordinate(latitude: float, longitude: float, distance_radius: float,
                              session: Session = Depends(get_session)):
    """

    Args:
        latitude: latitude of the location
        longitude: longitude of the location
        distance: distance radius
        session: database session

    Returns:
        list of all location which satisfy the distance criterion
    """
    if not ((-90 <= latitude <= 90) and (-180 <= longitude <= 180)):
        msg = f"The valid range of latitude is between -90 and 90\n" \
              f"The valid range of longitude is between -180 and -90"
        logger.error(msg)
        raise HTTPException(status_code=400, detail=msg)
    # store the latitude longitude value as a tuple
    location = (latitude, longitude)
    # initialize a list to store list of address within the given radius
    location_with_radius = []
    addresses = session.query(models.AddressEntry).all()
    for address in addresses:
        distance = haversine(location, (address.latitude, address.longitude))
        if distance < distance_radius:
            logger.info(f"{address.name} is within {distance_radius} KM of the given location")
            # append to the result list
            location_with_radius.append(address)
    return location_with_radius

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
