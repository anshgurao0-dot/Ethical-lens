from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from app.models.user_profile import UserProfile
from app.models.product_analysis import ProductAnalysis, TrafficLightStatus
from app.agents.researcher import ResearcherAgent
from app.agents.bio_shield import BioShieldAgent
from app.agents.judge import JudgeAgent
from app.agents.corporate_detective import CorporateDetectiveAgent
from app.agents.circular_guide import CircularGuideAgent
from app.agents.alternative_recommender import AlternativeRecommenderAgent
from app.agents.true_cost import TrueCostAgent
from app.agents.localvore import LocalvoreScoutAgent
from app.agents.activist import ActivistAgent

app = FastAPI(title="Ethical Lens Backend", version="0.1.0")

# Initialize Agents
researcher = ResearcherAgent()
bio_shield = BioShieldAgent()
judge = JudgeAgent()
corporate_detective = CorporateDetectiveAgent()
circular_guide = CircularGuideAgent()
alternative_recommender = AlternativeRecommenderAgent()
true_cost = TrueCostAgent()
localvore = LocalvoreScoutAgent()
activist = ActivistAgent()

class AnalyzeRequest(BaseModel):
    barcode: str
    user_profile: UserProfile
    image_data: Optional[str] = None # Base64 encoded image if needed

@app.get("/")
async def root():
    return {"message": "Ethical Lens Backend is running"}

@app.post("/analyze", response_model=ProductAnalysis)
async def analyze_product(request: AnalyzeRequest):
    """
    Orchestrates the analysis of a product by multiple agents.
    """
    print(f"Received analysis request for barcode: {request.barcode}")

    # 1. Researcher: Fetch Product Data
    # In a real scenario, we might pass the image_data to a Vision agent first if barcode is missing.
    product_data_verdict = await researcher.analyze({"barcode": request.barcode})
    
    # Extract the raw product data from the researcher's findings (mocked for now)
    # In reality, the researcher would return the raw data as part of its details or a separate object.
    # For this scaffold, we'll assume the 'details' contain the data we need for other agents.
    product_context = product_data_verdict.details
    
    # Add ingredients for other agents to use (Mocking data if not present)
    if "ingredients" not in product_context:
        product_context["ingredients"] = ["Sugar", "Palm Oil", "Peanuts"] # Mock ingredients

    # 2. Parallel Analysis: Bio-Shield and Judge
    # We pass the user profile and the product data found by the researcher
    context = {"user_profile": request.user_profile}
    
    bio_verdict = await bio_shield.analyze(product_context, context)
    judge_verdict = await judge.analyze(product_context, context)
    corporate_verdict = await corporate_detective.analyze(product_context, context)
    circular_verdict = await circular_guide.analyze(product_context, context)
    recommender_verdict = await alternative_recommender.analyze(product_context, context)
    true_cost_verdict = await true_cost.analyze(product_context, context)
    localvore_verdict = await localvore.analyze(product_context, context)
    activist_verdict = await activist.analyze(product_context, context)

    # 3. Aggregation
    verdicts = [product_data_verdict, bio_verdict, judge_verdict, corporate_verdict, circular_verdict, recommender_verdict, true_cost_verdict, localvore_verdict, activist_verdict]
    
    # Simple aggregation logic: Worst status wins (Red > Yellow > Green)
    overall_status = TrafficLightStatus.GREEN
    overall_score = 0.0
    
    has_red = any(v.status == TrafficLightStatus.RED for v in verdicts)
    has_yellow = any(v.status == TrafficLightStatus.YELLOW for v in verdicts)
    
    if has_red:
        overall_status = TrafficLightStatus.RED
        overall_score = min(v.score for v in verdicts) # Take the lowest score
    elif has_yellow:
        overall_status = TrafficLightStatus.YELLOW
        overall_score = sum(v.score for v in verdicts) / len(verdicts) # Average? Or lowest?
    else:
        overall_status = TrafficLightStatus.GREEN
        overall_score = sum(v.score for v in verdicts) / len(verdicts)

    return ProductAnalysis(
        product_id=request.barcode,
        product_name=product_context.get("product_name", "Unknown Product"),
        overall_score=overall_score,
        overall_status=overall_status,
        agent_verdicts=verdicts,
        timestamp="2025-12-01T12:00:00Z" # TODO: Use actual time
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
