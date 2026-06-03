from typing import TypedDict, Annotated, Sequence
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

# typedDict untuk mendefinisikan struktur dictionary yg memiliki key tertentu beserta tipe datanya

# sequence adalah tipe untuk data yg berurutan. Pada kode di bawah, messages berisi kumpulan data berurutan, yakni list chat messages
# yang berupa HumanMessage("Halo"),
#             AIMessage("Hai")

# annotated digunakan untuk menambahkan metadata pada tipe data. Pada kode di bawah, metadata yang ditambahkan adalah fungsi add_messages,
# yang digunakan untuk menambahkan pesan ke dalam graph state.
# Jadi, messages adalah sequence, dan ketika state diperbarui, fungsi add messages akan menggabungkan nilainya.
# Fungsinya adalah untuk menggabungkan pesan baru dengan pesan yang sudah ada sebelumnya dalam graph state.
# Tanpa add messages, pesan lama akan hilang

class AgentState(TypedDict):
    messages: Annotated[
        Sequence[BaseMessage], 
        add_messages
    ]
    # field messages berisi daftar chat (HumanMessage, AIMessage, dst.)
    # jika node menambahkan message baru, jangan hapus yg lama, tetapi tambahkan ke riwayat chat. 
    task_type: str
    retrieved_docs: str
    sentiment_result: str
    sentiment_result: str
    statistics_result: str
    final_answer: str