import os
from supabase import create_client, Client
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from ORtools import check_availabiliy

app = FastAPI()
SUPABASE_URL = "https://xoyzsjymkfcwtumzqzha.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhveXpzanlta2Zjd3R1bXpxemhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQyMTk4MTUsImV4cCI6MjA1OTc5NTgxNX0.VLMHbn4-rMaz9DWK1zcIJccWBnaQhrepek-umKH2s0Y"
url = SUPABASE_URL
key = SUPABASE_KEY
supabase: Client = create_client(url, key)

class Resource(BaseModel):
    name: str
    type: str

@app.get("/")
def read_root():
   response = supabase.table("Resources").select("*").eq("Resource_Name","MathBook").execute()
   return response


@app.post("/resource-insert/")
def insert_resource(resource: Resource):
    response = (
        supabase.table("Resources")
        .insert({
            "Resource_Name": resource.name,
            "Resource_Type": resource.type
        })
        .execute()
    )
    return response

class Booking (BaseModel):
    booked_by : str
    resource_name : str
    booking_period : int
    start : int
    end : int
    booked_date : str

@app.post("/create-booking")
def create_booking(booking : Booking):
   response1 = (
        supabase.table("Bookings").select("Booking_EndTime","Booking_StartTime")
        .eq("Booking_On",booking.booked_date).eq("Resource_Name",booking.resource_name)
        .execute()
    )
   startimes=[]
   endtimes=[]
   for x in response1.data:
      startimes.append(x["Booking_StartTime"])
      endtimes.append(x["Booking_EndTime"])
   available = check_availabiliy(startimes,endtimes,booking.start,booking.end)
   if available:
         response2 = (
            supabase.table("Bookings")
            .insert(
                  {
                     "Booked_By" : booking.booked_by,
                     "Resource_Name" : booking.resource_name,
                     "Booking_Period" : booking.booking_period,
                     "Booking_StartTime" : booking.start,
                     "Booking_EndTime" : booking.end,
                     "Booking_On" : booking.booked_date
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
    response_1 = (supabase.table("Bookings").select("id").eq("Resource_Name",request.old_booking.resource_name).eq("Booking_On",request.old_booking.booked_date)
                  .eq("Booking_StartTime",request.old_booking.start).eq("Booking_EndTime",request.old_booking.end).execute())
    
    current_booking_id = response_1.data[0]["id"]
    
    response_2 = (
        supabase.table("Bookings").select("Booking_EndTime","Booking_StartTime")
        .eq("Booking_On",request.new_booking.booked_date).eq("Resource_Name",request.new_booking.resource_name).neq("id",current_booking_id)
        .execute()
    )
    startimes=[]
    endtimes=[]
    for x in response_2.data:
       startimes.append(x["Booking_StartTime"])
       endtimes.append(x["Booking_EndTime"])
    available = check_availabiliy(startimes,endtimes,request.new_booking.start,request.new_booking.end)
    if available:
       supabase.table("Bookings") \
        .update({
        "Booked_By": request.new_booking.booked_by,
        "Resource_Name": request.new_booking.resource_name,
        "Booking_Period": request.new_booking.booking_period,
        "Booking_StartTime": request.new_booking.start,
        "Booking_EndTime": request.new_booking.end,
        "Booking_On": request.new_booking.booked_date
    }) \
    .eq("id", current_booking_id) \
    .execute()
       print("booking modified successfully")
    else:
        print("Resource not available on the specified time slot")


   

    