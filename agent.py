from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from tools import search_flights, search_hotels, calculate_budget
from dotenv import load_dotenv

load_dotenv()

# 1. Đọc System Prompt
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# 2. Khai báo State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 3. Khởi tạo LLM và Tools
tools_list = [search_flights, search_hotels, calculate_budget]
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools_list)

# 4. Agent Node
def agent_node(state: AgentState):
    messages = state["messages"]
    
    # Thêm System Prompt vào đầu danh sách tin nhắn nếu chưa có
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    response = llm_with_tools.invoke(messages)
    
    # === LOGGING ===
    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"Gọi tool: {tc['name']}({tc['args']})")
    else:
        print(f"Trả lời trực tiếp")

    return {"messages": [response]}

# 5. Xây dựng Graph
builder = StateGraph(AgentState)

# Thêm các Node (Nút xử lý)
builder.add_node("agent", agent_node) # Nút xử lý logic của AI

tool_node = ToolNode(tools_list)  # Nút thực thi các công cụ (search_flights,...)
builder.add_node("tools", tool_node)

# TODO: Sinh viên khai báo edges

# Định nghĩa các Edges (Luồng di chuyển)
# Bắt đầu luôn đi vào nút agent
builder.add_edge(START, "agent")

# Sau khi agent xử lý, dùng tools_condition để quyết định:
# - Nếu LLM yêu cầu gọi tool -> chuyển sang nút "tools"
# - Nếu LLM trả lời thẳng người dùng -> kết thúc (END)
builder.add_conditional_edges("agent", tools_condition)

# Sau khi thực thi tool xong, PHẢI quay lại agent để AI đọc kết quả và phản hồi
builder.add_edge("tools", "agent")

# Biên dịch đồ thị thành một ứng dụng có thể chạy được
graph = builder.compile()

# 6. Chat loop
if __name__ == "__main__":
    print("=" * 60)
    print("TravelBuddy - Trợ lý Du lịch Thông minh")
    print("      Gõ 'quit' để thoát")
    print("=" * 60)

    while True:
        user_input = input("\nBạn: ").strip()
        if user_input.lower() in ["quit", "exit", "q"]:
            break

        # Blacklist để ngăn chặn người dùng cố tình bypass hệ thống bằng cách yêu cầu AI "quên các quy tắc" hoặc "ignore previous instructions"
        blacklist = ["ignore previous instructions", "quên các quy tắc", "hệ thống quản trị"]
        if any(word in user_input.lower() for word in blacklist):
            print("TravelBuddy: Phát hiện yêu cầu không hợp lệ. Vui lòng hỏi về du lịch!")
            continue
        
        print("\nTravelBuddy đang suy nghĩ...")
        result = graph.invoke({"messages": [("human", user_input)]})
        final = result["messages"][-1]
        print(f"\nTravelBuddy: {final.content}")