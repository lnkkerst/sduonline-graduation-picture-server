from fastapi import HTTPException
import httpx
import re


async def login_sdu(sdu_id: str, password: str):
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                "https://pass.sdu.edu.cn/cas/restlet/tickets",
                data=f"username={sdu_id}&password={password}",  # type: ignore
            )
            if not str(res.status_code).startswith("2"):
                return None
            res = await client.post(
                f"https://pass.sdu.edu.cn/cas/restlet/tickets/{res.text.strip()}",
                data="service=http://bkzhjx.wh.sdu.edu.cn/sso.jsp",  # type: ignore
            )
            res = await client.get(
                f"https://pass.sdu.edu.cn/cas/serviceValidate?ticket={res.text.strip()}&service=http://bkzhjx.wh.sdu.edu.cn/sso.jsp"
            )
            name = re.match(
                r".*<cas:USER_NAME>(.*)</cas:USER_NAME>.*", res.text, flags=re.M | re.S
            ).group(  # type: ignore
                1
            )
            return {"name": name}
    except Exception:
        raise HTTPException(status_code=401, detail="Authorization failed")
