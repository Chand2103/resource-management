import os
from supabase import create_client, Client
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, Depends,Request,Query
from fastapi.middleware.cors import CORSMiddleware
from .or_tools import check_availabiliy
import json
from datetime import date
from datetime import time
from .dependencies.auth import get_current_user



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all domains (be careful for production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


SUPABASE_URL = "https://xoyzsjymkfcwtumzqzha.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhveXpzanlta2Zjd3R1bXpxemhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQyMTk4MTUsImV4cCI6MjA1OTc5NTgxNX0.VLMHbn4-rMaz9DWK1zcIJccWBnaQhrepek-umKH2s0Y"
url = SUPABASE_URL
key = SUPABASE_KEY
supabase: Client = create_client(url, key)



class Resource(BaseModel):
    name: str
    type: str
    capacity :int
    location : str

@app.get("/")
def read_root():
    print("resource-management-services are running")

@app.get("/get-resources")
def get_resources():
    return supabase.table("Resources").select("*").execute().data

@app.post("/resource-insert")
def insert_resource(resource: Resource):
    response = (
        supabase.table("Resources")
        .insert({
            "resource_name": resource.name,
            "resource_type": resource.type,
            "capacity":resource.capacity,
            "location":resource.location
        })
        .execute()
    )
    return response
class ResourceUpdate(BaseModel):
    name: str
    type: str
    capacity: int
    location :str

@app.put("/resource-update/{resource_id}")
def update_resource(resource_id: int, updated_resource: ResourceUpdate):
    response = (
        supabase.table("Resources")
        .update({
            "resource_name": updated_resource.name,
            "resource_type": updated_resource.type,
            "capacity": updated_resource.capacity,
            "location":updated_resource.location
        })
        .eq("id", resource_id)
        .execute()
    )
    
    if len(response.data) == 0:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    return {"message": "Resource updated successfully", "data": response.data}

@app.delete("/resource-delete/{resource_id}")
def delete_resource(resource_id: str):
    response = (
        supabase.table("Resources")
        .delete()
        .eq("id", resource_id)
        .execute()
    )
    return response

class Booking (BaseModel):
    booked_by : str
    resource_name : str
    start : str
    end : str
    booked_date : str

@app.post("/create-booking")
def create_booking(booking : Booking):
   response1 = (
        supabase.table("Bookings").select("booking_endtime","booking_starttime")
        .eq("booking_on",booking.booked_date).eq("resource_name",booking.resource_name)
        .execute()
    )
   startimes=[]
   endtimes=[]
   for x in response1.data:
      startimes.append(x["booking_starttime"])
      endtimes.append(x["booking_endtime"])
   available = check_availabiliy(startimes,endtimes,booking.start,booking.end)
   if available:
         response2 = (
            supabase.table("Bookings")
            .insert(
                  {
                     "booked_by" : booking.booked_by,
                     "resource_name" : booking.resource_name,
                     "booking_starttime" : booking.start,
                     "booking_endtime" : booking.end,
                     "booking_on" : booking.booked_date
                  }
            ).execute()
         )
         print("booking done successfully")
         return {"booking_id": response2.data[0]["id"]}
   else:
       print("Resource not available on the specified time slot")
       return {"error": "Resource not available on the specified time slot"}


class UpdateBookingRequest(BaseModel):
    id: int
    date: str
    startTime: str
    endTime: str
    # add any other fields you want to update

@app.put("/booking-update")
def update_booking(request: UpdateBookingRequest):
    # Replace this with your actual DB update logic using Supabase or ORM
    response = supabase.table("Bookings").update({
        "booking_on": request.date,
        "booking_starttime": request.startTime,
        "booking_endtime": request.endTime,
        # other fields here
    }).eq("id", request.id).execute()

    if response.data:
        return response.data[0]  # return updated booking


@app.get("/get-bookings")
def get_resources():
    return supabase.table("Bookings").select("*").execute().data

@app.get("/get-bookings-user")
def get_resources(userid: str = Query(...)):
    return supabase.table("Bookings").select("*").eq("booked_by",userid).execute().data
    
@app.get("/get-bookings-resource") ##this api endpoint is associated with the IoT part
def get_bookings(resource_name: str, booked_date: str):
    response1 = (
        supabase.table("Bookings").select("booking_endtime","booking_starttime","id")
        .eq("booking_on",booked_date).eq("resource_name",resource_name)
        .execute()
    )
    startimes = []
    endtimes = []
    ids = []
    for x in response1.data:
       startimes.append(x["booking_starttime"])
       endtimes.append(x["booking_endtime"])
       ids.append(x["id"])

    data = {
    "startimes": startimes,
    "endtimes": endtimes,
    "ids": ids
    }

    return data

class DeleteBookingRequest(BaseModel):
    booking_id: int

@app.delete("/delete-booking")
def delete_booking(request: DeleteBookingRequest):
    response = supabase.table("Bookings").delete().eq("id", request.booking_id).execute()

    if response.data:
        return {"status": "success", "message": f"Booking ID {request.booking_id} deleted."}
    else:
        return {"status": "error", "message": "Booking not found or deletion failed."}


@app.get("/check-availability")
def check_availability(resource_name : str ,booking_date :str):
    response = (
    supabase.table("Bookings")
    .select("booking_endtime", "booking_starttime")
    .eq("resource_name", resource_name)
    .eq("booking_on", booking_date)
    .execute()
    )

    already_booked = []

    for x in response.data:
        time_slot = f"{x['booking_starttime']} : {x['booking_endtime']}"
        already_booked.append(time_slot)
    return already_booked


class Person(BaseModel):
    name:str
    occupation:str
    contact_number:str

@app.get("/get-people")
def get_people():
    return supabase.table("People").select("*").execute().data


@app.post("/add-people")
def add_people(person:Person):
    (
            supabase.table("People")
            .insert(
                  {
                     "name" : person.name,
                     "occupation" : person.occupation,
                     "contact_number" : person.contact_number,

                  }
            ).execute()
         )


@app.put("/assign-people")
def assign_people(person_id : int,resource: int):
        (
            supabase.table("People")
            .update(
                  {
                     "resource_assigned":resource
                  }
            )
            .eq('id',person_id)
            .execute()
         )
    
