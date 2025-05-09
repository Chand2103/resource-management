import os
from supabase import create_client, Client
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ORtools import check_availabiliy
import json
from datetime import date
from datetime import time

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

@app.get("/")
def read_root():
   response = supabase.table("Resources").select("*").execute()
   return response

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
            "capacity":resource.capacity
        })
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
   else:
       print("Resource not available on the specified time slot")


class ModifyBookingRequest(BaseModel):
    new_booking: Booking
    old_booking: Booking



@app.post("/modify-booking")
def modify_booking(request : ModifyBookingRequest):
    response_1 = (supabase.table("Bookings").select("id").eq("resource_name",request.old_booking.resource_name).eq("booking_on",request.old_booking.booked_date)
                  .eq("booking_starttime",request.old_booking.start).eq("booking_endtime",request.old_booking.end).execute())
    
    current_booking_id = response_1.data[0]["id"]
    
    response_2 = (
        supabase.table("Bookings").select("booking_endtime","booking_starttime")
        .eq("booking_on",request.new_booking.booked_date).eq("resource_name",request.new_booking.resource_name).neq("id",current_booking_id)
        .execute()
    )
    startimes=[]
    endtimes=[]
    for x in response_2.data:
       startimes.append(x["booking_starttime"])
       endtimes.append(x["booking_endtime"])
    available = check_availabiliy(startimes,endtimes,request.new_booking.start,request.new_booking.end)
    if available:
       supabase.table("Bookings") \
        .update({
        "booked_by": request.new_booking.booked_by,
        "resource_name": request.new_booking.resource_name,
        "booking_starttime": request.new_booking.start,
        "booking_endtime": request.new_booking.end,
        "booking_on": request.new_booking.booked_date
    }) \
    .eq("id", current_booking_id) \
    .execute()
       print("booking modified successfully")
    else:
        print("Resource not available on the specified time slot")


@app.get("/get-bookings")
def get_resources():
    return supabase.table("Bookings").select("*").execute().data
    
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
        time_slot = f"{x["booking_starttime"]} : {x["booking_endtime"]}"
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
    print("booking done successfully")


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
    