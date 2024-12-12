#py -m uvicorn main:app --reload
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime
from typing import Annotated,Optional
from pydantic import BaseModel
import uuid



app = FastAPI()
templates = Jinja2Templates(directory="templates")
alerts=[]


class Order(BaseModel):
    id: uuid.UUID = uuid.uuid4()
    Number: int
    data: Optional[datetime] = datetime.now()
    enddata: Optional[datetime] = None
    OrgTex: str
    Model: str
    Opisanie: str
    fio: str
    tel: str
    status: str
    etap: str = None
    master: str = None
    com: list = None

    def clear(self) -> None:
        self.id = None
        self.Number = None
        self.data = None
        self.enddata = None
        self.OrgTex = None
        self.Model = None
        self.Opisanie = None
        self.fio = None
        self.tel = None
        self.status = None
        self.etap = None
        self.master = None
        self.com = None

class UpdateDTO(BaseModel):
    id: uuid.UUID = None
    Number: int
    status: str
    etap: str
    Opisanie: str = ""
    master: str = ""
    com: list = ""

    def clear(self) -> None:
        self.id = None
        self.Number = None
        self.status = None
        self.etap = None
        self.Opisanie = None
        self.master = None
        self.com = None


repo = [
        Order(
        Number=1,
        OrgTex="1",
        Model="1",
        Opisanie="1",
        fio="1",
        tel="1",
        status="в процессе ремонта",
        etap="в процессе ремонта",
        master="1",
        com=[]),

        Order(
        Number=2,
        OrgTex="2",
        Model="2",
        Opisanie="2",
        fio="2",
        tel="2",
        status="в процессе ремонта",
        etap="в процессе ремонта",
        master="2",
        com=[]),

        Order(
        Number=3,
        OrgTex="3",
        Model="3",
        Opisanie="3",
        fio="3",
        tel="3",
        status="в процессе ремонта",
        etap="в процессе ремонта",
        master="3",
        com=[])
        ]


@app.post("/create", response_class=HTMLResponse)
def create(request: Request, dto:Annotated[Order, Form()]):
    repo.append(dto)
    return templates.TemplateResponse("repo.html", {"request": request, "orders": repo, "alerts": alerts})

@app.post("/update", response_class=HTMLResponse)
def update(request: Request, dto : Annotated[UpdateDTO, Form()]):
    global alerts
    for i in repo:
        print(i)
        if i.Number == dto.Number:
            if i.status != dto.status:
                alerts.append(f"Заявка по {i.Number} изменена на {i.status}")
            i.status = dto.status
            i.etap = dto.etap
            if i.status == "завершена" and i.etap == "готова к выдаче":
                i.enddata = datetime.now()
            i.Opisanie = dto.Opisanie
            i.master = dto.master
            return templates.TemplateResponse("repo.html", {"request": request, "orders": repo, "alerts": alerts})
        return "Не верный  Номер заявки"

@app.get("/repo", response_class=HTMLResponse)
def repo_view(request: Request):
    return templates.TemplateResponse("repo.html", {"request": request, "orders": repo, "alerts": alerts})





