import httpx
from typing import Optional
from sport_oracle.config import FOOTBALL_DATA_API_KEY, FOOTBALL_DATA_BASE_URL


HEADERS = {"X-Auth-Token": FOOTBALL_DATA_API_KEY}


async def get_live_scores() -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{FOOTBALL_DATA_BASE_URL}/matches",
            headers=HEADERS,
            params={"status": "LIVE,IN_PLAY,PAUSED"},
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()


async def get_todays_matches() -> dict:
    from datetime import date
    today = date.today().isoformat()
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{FOOTBALL_DATA_BASE_URL}/matches",
            headers=HEADERS,
            params={"dateFrom": today, "dateTo": today},
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()


async def get_competition_matches(competition_code: str, matchday: Optional[int] = None) -> dict:
    params: dict = {"status": "SCHEDULED,LIVE,IN_PLAY,PAUSED,FINISHED"}
    if matchday:
        params["matchday"] = matchday
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{FOOTBALL_DATA_BASE_URL}/competitions/{competition_code}/matches",
            headers=HEADERS,
            params=params,
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()


async def get_team_info(team_id: int) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{FOOTBALL_DATA_BASE_URL}/teams/{team_id}",
            headers=HEADERS,
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()


async def get_competition_standings(competition_code: str) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{FOOTBALL_DATA_BASE_URL}/competitions/{competition_code}/standings",
            headers=HEADERS,
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()


async def search_team(name: str) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{FOOTBALL_DATA_BASE_URL}/teams",
            headers=HEADERS,
            params={"name": name, "limit": 5},
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()


async def get_match(match_id: int) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{FOOTBALL_DATA_BASE_URL}/matches/{match_id}",
            headers=HEADERS,
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()


async def get_head_to_head(match_id: int) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{FOOTBALL_DATA_BASE_URL}/matches/{match_id}/head2head",
            headers=HEADERS,
            params={"limit": 10},
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()


def format_score(match: dict) -> str:
    home = match["homeTeam"]["name"]
    away = match["awayTeam"]["name"]
    score = match.get("score", {})
    ft = score.get("fullTime", {})
    ht = score.get("halfTime", {})
    status = match.get("status", "")

    home_goals = ft.get("home")
    away_goals = ft.get("away")

    if home_goals is not None and away_goals is not None:
        score_str = f"{home_goals} - {away_goals}"
    else:
        score_str = "? - ?"

    if status in ("LIVE", "IN_PLAY", "PAUSED"):
        minute = match.get("minute", "")
        tag = f"🔴 LIVE {minute}'" if minute else "🔴 LIVE"
    elif status == "FINISHED":
        tag = "✅ FT"
    elif status == "SCHEDULED":
        utc_date = match.get("utcDate", "")
        tag = f"🕐 {utc_date[11:16]} UTC" if utc_date else "🕐"
    else:
        tag = status

    competition = match.get("competition", {}).get("name", "")
    return f"{tag} | {competition}\n{home} {score_str} {away}"
