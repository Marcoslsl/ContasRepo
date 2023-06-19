from fastapi import APIRouter
from .endpoints.contas_a_pagar_e_receber import router as contas_pagar

router = APIRouter()
router.include_router(contas_pagar)
