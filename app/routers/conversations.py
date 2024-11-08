from urllib.parse import urlencode
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.services.conversation_service import ConversationService
from fastapi.responses import JSONResponse

router = APIRouter()
conversation_service = ConversationService()

@router.post("/conversations/",
             tags=["conversations"],
             responses={
                 201: {"description": "Conversation created successfully"},
                 400: {"description": "Bad request - invalid parameters"},
                 409: {"description": "Conflict - conversation already exists"}
             })
def create_conversation(conversation: dict):
    try:
        conversation_id = conversation_service.create_conversation(conversation)
        return JSONResponse(content={"convo_id": conversation_id ["convo_id"], "detail": "Conversation created successfully"}, status_code=201)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating conversation: {str(e)}")

@router.put("/conversations/{conversation_id}",
            tags=["conversations"],
            responses={
                200: {"description": "Conversation updated successfully"},
                404: {"description": "Conversation not found"},
                400: {"description": "Bad request - invalid parameters"}
            })
def update_conversation(conversation_id: int, conversation: dict):
    try:
        conversation_service.update_conversation(conversation_id, conversation)
        return JSONResponse(content={"detail": "Conversation updated successfully"}, status_code=200)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations/{conversation_id}",
            tags=["conversations"],
            responses={
                200: {"description": "Conversation retrieved successfully"},
                404: {"description": "Conversation not found"},
                400: {"description": "Bad request - invalid parameters"}
            })
def get_conversation(conversation_id: int):
    try:
        conversation = conversation_service.get_conversation(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return JSONResponse(content={"detail": conversation}, status_code=200)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/",
            tags=["conversations"],
            responses={
                200: {"description": "Conversation retrieved successfully"},
                404: {"description": "Conversation not found"},
                400: {"description": "Bad request - invalid parameters"}
            })
def get_all_conversations():
    try:
        conversations = conversation_service.get_all_conversations()
        if not conversations:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return JSONResponse(content={"detail": conversations}, status_code=200)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/conversations/{conversation_id}",
               tags=["conversations"],
               responses={
                   200: {"description": "Conversation deleted successfully"},
                   404: {"description": "Conversation not found"},
                   400: {"description": "Bad request - invalid parameters"}
               })
def delete_conversation(conversation_id: int):
    try:
        conversation_service.delete_conversation(conversation_id)
        return JSONResponse(content={"detail": "Conversation deleted successfully"}, status_code=200)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))