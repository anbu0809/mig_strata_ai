from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from enum import Enum

class DatabaseType(str, Enum):
    POSTGRESQL = "PostgreSQL"
    MYSQL = "MySQL"
    SNOWFLAKE = "Snowflake"
    DATABRICKS = "Databricks"
    ORACLE = "Oracle"
    SQL_SERVER = "SQL Server"
    TERADATA = "Teradata"
    BIGQUERY = "Google BigQuery"

class ConnectionTestRequest(BaseModel):
    dbType: DatabaseType
    name: str
    credentials: Dict[str, Any]

class ConnectionTestResponse(BaseModel):
    ok: bool
    vendorVersion: Optional[str] = None
    details: Optional[str] = None

class ConnectionSaveRequest(BaseModel):
    dbType: DatabaseType
    name: str
    credentials: Dict[str, Any]

class ConnectionSaveResponse(BaseModel):
    ok: bool
    id: Optional[int] = None

class ConnectionResponse(BaseModel):
    id: int
    name: str
    dbType: str

class SetSourceTargetRequest(BaseModel):
    sourceId: int
    targetId: int

class SessionResponse(BaseModel):
    source: Optional[ConnectionResponse] = None
    target: Optional[ConnectionResponse] = None

class AnalysisStatusResponse(BaseModel):
    ok: bool
    phase: Optional[str] = None
    percent: Optional[int] = None
    done: Optional[bool] = None
    resultsSummary: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class CommonResponse(BaseModel):
    ok: bool
    message: Optional[str] = None
    data: Optional[Any] = None