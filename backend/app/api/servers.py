"""
Server API routes
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.connection import get_db
from app.services.server_service import ServerService
from app.models.schemas import Server, ServerCreate, ServerUpdate

router = APIRouter(prefix="/servers", tags=["Servers"])


@router.get("/", response_model=List[Server])
async def list_servers(
    restaurant_id: Optional[str] = Query(None, description="Filter servers by restaurant ID"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db)
):
    """List all servers"""
    service = ServerService(db)
    return service.get_servers(restaurant_id=restaurant_id, is_active=is_active)


@router.post("/", response_model=Server, status_code=201)
async def create_server(
    server_data: ServerCreate,
    db: Session = Depends(get_db)
):
    """Create a new server"""
    service = ServerService(db)
    return service.create_server(server_data)


@router.get("/{server_id}", response_model=Server)
async def get_server(
    server_id: str,
    db: Session = Depends(get_db)
):
    """Get server by ID"""
    service = ServerService(db)
    server = service.get_server(server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return server


@router.put("/{server_id}", response_model=Server)
async def update_server(
    server_id: str,
    server_data: ServerUpdate,
    db: Session = Depends(get_db)
):
    """Update server"""
    service = ServerService(db)
    server = service.update_server(server_id, server_data)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return server


@router.delete("/{server_id}", status_code=204)
async def delete_server(
    server_id: str,
    db: Session = Depends(get_db)
):
    """Delete server"""
    service = ServerService(db)
    if not service.delete_server(server_id):
        raise HTTPException(status_code=404, detail="Server not found")
