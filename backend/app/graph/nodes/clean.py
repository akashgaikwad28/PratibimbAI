from bs4 import BeautifulSoup
from app.utils.metrics import instrument_node
from app.graph.state import GraphState
from app.utils.logger import get_logger
from app.core.constants import MAX_CONTENT_LENGTH

logger = get_logger(__name__)


@instrument_node("clean")
def clean_node(state: GraphState):
    cleaned_contents = []
    for html in state.raw_contents:
        if html.startswith("ERROR"):
            cleaned_contents.append(html)
            continue
        try:
            soup = BeautifulSoup(html, "html.parser")
            for tag in soup(["nav", "footer", "script", "style", "header"]):
                tag.decompose()
            text = soup.get_text(separator=" ", strip=True)
            cleaned_contents.append(text[:MAX_CONTENT_LENGTH])
        except Exception as e:
            error_msg = f"Clean failed: {e}"
            state.errors.append(error_msg)
            logger.error(f"[{state.execution_id}] {error_msg}")
    return {"clean_contents": cleaned_contents, "errors": state.errors}
