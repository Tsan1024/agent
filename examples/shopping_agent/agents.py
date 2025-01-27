from src.agent.shopping_agent import shopping
from swarm import Agent

def shopping_action(item:str):
    shopping(item)
    return "finish"

def process_refund(item_id, reason="NOT SPECIFIED"):
    """Refund an item. Refund an item. Make sure you have the item_id of the form item_... Ask for user confirmation before processing the refund."""
    print(f"[mock] Refunding item {item_id} because {reason}...")
    return "Success!"


def apply_discount():
    """Apply a discount to the user's cart."""
    print("[mock] Applying discount...")
    return "Applied discount of 11%"


choice_captain_agent = Agent(
    name="choice_caption_agent",
    instructions="""你是一个agent选择助手，确定哪个agent最适合处理用户的请求，并将对话转接给该agent。目前有两个agent:
    一个是shopping_agent专注于执行用户的购买和收藏操作。主要任务是帮助用户将选择的商品加入购物车或加入收藏夹。 
    另一个是recommendation_agent专注于商品推荐。
    你需要根据用户请求信息确定哪个agent最适合处理用户的请求，并将任务转接给该agent。
    """,
)
shopping_agent = Agent(
    name="shopping_agent",
    instructions="""
    你是一个购物助手，专注于执行用户的购买和收藏操作。你的主要任务是帮助用户将选择的商品加入购物车或加入收藏夹。如果有超过能力范围外的技能如推荐商品则交给recommendation_agent或者choice_caption_agent处理。
    功能包含：
    1. 获取用户的需要的商品，添加到购物车。
    2. 获取用户的需要的商品，添加到收藏。
    专注于购物功能。
    """,
    functions=[shopping_action],
)

recommendation_agent = Agent(
    name="recommendation_agent",
    instructions="""
    你是一个推荐专家。你的任务是根据用户的需求，帮助他们推荐最合适的商品,如果有超过能力范围外的比如将商品加入购物车则交给shopping_agent或者choice_caption_agent处理。

    功能包含：
    1. 获取用户的需求和偏好，包括预算、品牌偏好、特定功能需求等。
    2. 比较不同产品的优缺点，并根据用户的需求推荐最佳商品。
    3. 在推荐中，考虑性价比并推荐最有性价比的一款产品。
    4. 最后询问用户是否可以接受推荐的品牌和商品。
    5. 如果用户接受推荐的商品则交由或者choice_caption_agent或shopping_agent执行加入购物车。

    请确保推荐的商品符合用户的需求，并提供清晰的理由和详细信息，帮助用户做出购买决策。
    """,
    functions=[process_refund, apply_discount],
)

# product_recommendation_agent = Agent(
#     name="product recommendation agent",
#     instructions="""
#     你是一个好物推荐专家。你的任务是根据用户的需求，帮助他们推荐和购买最合适的商品。
#
#     功能包含：
#     1. 获取用户的需求和偏好，包括预算、品牌偏好、特定功能需求等。
#     2. 比较不同产品的优缺点，并根据用户的需求推荐最佳商品。
#     3. 提供详细的产品信息，包括价格、主要功能、用户评价等。
#     4. 根据用户的反馈，进一步优化推荐，直到用户满意为止。
#     5. 在推荐中，考虑性价比并推荐最有性价比的一款产品。
#     6. 最后询问用户是否可以接受推荐的品牌和商品。
#
#     请确保推荐的商品符合用户的需求，并提供清晰的理由和详细信息，帮助用户做出购买决策。
#     """,
#     functions=[process_refund, apply_discount],
# )


def transfer_back_to_triage():
    """Call this function if a user is asking about a topic that is not handled by the current agent."""
    return choice_captain_agent


def transfer_to_shopping():
    return shopping_agent


def transfer_to_recommendation_agent():
    return recommendation_agent


choice_captain_agent.functions = [transfer_to_shopping, transfer_to_recommendation_agent]
shopping_agent.functions.append(transfer_back_to_triage)
recommendation_agent.functions.append(transfer_back_to_triage)
