from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, JSONResponse
from app.config import settings
from app.dao.dao import MasterDAO, ServiceDAO, ApplicationDAO, UserDAO

router = APIRouter(prefix='', tags=['Фронтенд'])
templates = Jinja2Templates(directory='app/templates')


@router.get("/", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("index.html",
                                      {"request": request, "title": "Элегантная парикмахерская"})


@router.get("/form", response_class=HTMLResponse)
async def get_form(request: Request, user_id: int = None, first_name: str = None):
    masters = await MasterDAO.find_all()
    services = await ServiceDAO.find_all()
    data_page = {"request": request,
                 "user_id": user_id,
                 "first_name": first_name,
                 "title": "Запись на услуги - Элегантная парикмахерская",
                 "masters": masters,
                 "services": services}
    return templates.TemplateResponse("form.html", data_page)


@router.get("/admin", response_class=HTMLResponse)
async def get_admin(request: Request, admin_id: int = None):
    data_page = {"request": request, "access": False, 'title_h1': "Панель администратора"}
    if admin_id is None or admin_id not in settings.ADMIN_IDS:
        data_page['message'] = 'У вас нет прав для получения информации о заявках!'
        return templates.TemplateResponse("user_applications.html", data_page)
    else:
        data_page['access'] = True
        data_page['applications'] = await ApplicationDAO.get_all_applications()
        return templates.TemplateResponse("admin_applications.html", data_page)

@router.get("/archive/admin", response_class=HTMLResponse)
async def get_archive(request: Request, admin_id: int = None):
    data_page = {"request": request, "access": False, 'title_h1': "Панель администратора"}
    if admin_id is None or admin_id not in settings.ADMIN_IDS:
        data_page['message'] = 'У вас нет прав для получения информации о заявках!'
        return templates.TemplateResponse("user_applications.html", data_page)
    else:
        data_page['access'] = True
        data_page['applications'] = await ApplicationDAO.get_all_applications(archive=True)
        return templates.TemplateResponse("admin_applications.html", data_page)


@router.get("/applications", response_class=HTMLResponse)
async def get_applications(request: Request, user_id: int = None):
    data_page = {"request": request, "access": False, 'title_h1': "Мои записи"}
    user_check = await UserDAO.find_one_or_none(telegram_id=user_id)

    if user_id is None or user_check is None:
        data_page['message'] = 'Пользователь по которому нужно отобразить заявки не указан или не найден в базе данных'
    else:
        applications = await ApplicationDAO.get_applications_by_user(user_id=user_id)
        data_page['access'] = True
        if applications and len(applications):
            data_page['applications'] = applications
        else:
            data_page['message'] = 'У вас нет заявок!'

    return templates.TemplateResponse("user_applications.html", data_page)

@router.post("/applications/close", response_class=HTMLResponse)
async def close_application(request: Request, application_id: int = None):
    data_page = {"request": request, "access": False, 'title_h1': "Мои записи"}
    app = await ApplicationDAO.update(filter_by={"id": application_id}, **{"is_closed": True})

@router.post("/applications/remove", response_class=HTMLResponse)
async def remove_application(application_id: int = None):
    await ApplicationDAO.delete(delete_all=False, id=application_id)

@router.get("/service", response_class=HTMLResponse)
async def get_service(request: Request, admin_id: int = None):
    data_page = {"request": request, "access": False, 'title_h1': "Добавление услуги"}
    if admin_id is None or admin_id not in settings.ADMIN_IDS:
        data_page['message'] = 'У вас нет прав для получения информации об услугах!'
        return templates.TemplateResponse("services_error.html", data_page)
    else:
        data_page['access'] = True
        data_page['services'] = await ServiceDAO.find_all()
        return templates.TemplateResponse("services.html", data_page)

@router.post("/add/service")
async def add_service(service_name: str = None):
    try:
        await ServiceDAO.add(service_name=service_name)
        return JSONResponse(
            content={
                "success": True,
                "message": "Услуга успешно добавлена"
            },
            status_code=201
        )
    except Exception as e:
        return JSONResponse(
            content={
                "success": False,
                "message": f"Ошибка при добавлении услуги: {str(e)}"
            },
            status_code=400
        )

@router.post("/delete/service")
async def delete_service(service_id: int = None):
    try:
        await ServiceDAO.delete(service_id=service_id)
        return JSONResponse(
            content={
                "success": True,
                "message": "Услуга успешно удалена"
            },
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={
                "success": False,
                "message": f"Ошибка при удалении услуги: {str(e)}"
            },
            status_code=400
        )

@router.get("/masters", response_class=HTMLResponse)
async def get_masters(request: Request, admin_id: int = None):
    data_page = {"request": request, "access": False, 'title_h1': "Добавление мастера"}
    if admin_id is None or admin_id not in settings.ADMIN_IDS:
        data_page['message'] = 'У вас нет прав для получения информации об услугах!'
        return templates.TemplateResponse("services_error.html", data_page)
    else:
        data_page['access'] = True
        data_page['masters'] = await MasterDAO.find_all()
        return templates.TemplateResponse("masters.html", data_page)

@router.post("/add/master")
async def add_master(master_name: str = None):
    try:
        await MasterDAO.add(master_name=master_name)
        return JSONResponse(
            content={
                "success": True,
                "message": "Мастер успешно добавлен"
            },
            status_code=201
        )
    except Exception as e:
        return JSONResponse(
            content={
                "success": False,
                "message": f"Ошибка при добавлении мастера: {str(e)}"
            },
            status_code=400
        )

@router.post("/delete/master")
async def delete_master(master_id: int = None):
    try:
        await MasterDAO.delete(master_id=master_id)
        return JSONResponse(
            content={
                "success": True,
                "message": "Мастер успешно удален"
            },
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={
                "success": False,
                "message": f"Ошибка при удалении мастера: {str(e)}"
            },
            status_code=400
        )