from mcp.server.fastmcp import FastMCP
import traceback
from sentence_transformers import SentenceTransformer
import os
import fitz  # PyMuPDF
import faiss
import numpy as np

mcp = FastMCP("docreader")

# 벡터DB
def build_or_load_index(chunks):
    if not chunks:
        raise ValueError("No document chunks available for indexing")
    vectors = get_embeddings(chunks)
    dim = len(vectors[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(vectors))
    return index, chunks

def search_similar_chunks(query, index, chunks, top_k=5):
    q_vec = get_embeddings([query])
    _, idxs = index.search(np.array(q_vec), top_k)
    return [chunks[i] for i in idxs[0]]

# 텍스트 추출
def extract_text_from_pdf(file_path):
    with fitz.open(file_path) as doc:
        return "\n".join(page.get_text() for page in doc)

def split_into_chunks(text, chunk_size=300):
    sentences = text.split("\n")
    chunks, chunk = [], ""
    for sentence in sentences:
        if len(chunk) + len(sentence) < chunk_size:
            chunk += sentence + "\n"
        else:
            chunks.append(chunk.strip())
            chunk = sentence + "\n"
    if chunk:
        chunks.append(chunk.strip())
    return chunks

def load_and_chunk_documents(doc_dir):
    if not os.path.exists(doc_dir):
        raise FileNotFoundError(f"Document directory '{doc_dir}' does not exist")

    all_chunks = []
    for file in os.listdir(doc_dir):
        if file.lower().endswith(".pdf"):
            full_path = os.path.join(doc_dir, file)
            raw_text = extract_text_from_pdf(full_path)
            chunks = split_into_chunks(raw_text)
            all_chunks.extend(chunks)
    return all_chunks

# 임베딩
model = SentenceTransformer("all-MiniLM-L6-v2")  # 허깅페이스에서 제공하는 임베딩 모델
                                                 # 다른 모델로 변경 가능
def get_embeddings(chunks):
    return model.encode(chunks)

# Tool 등록
@mcp.tool(name="query_documents", description="PDF 문서를 검색하고 Claude에 질문을 전달합니다.")
def query_documents(query: str) -> str:
    try:
        print(f"[질문] {query}")
        docs = load_and_chunk_documents("docs/")  
        index, chunks = build_or_load_index(docs)
        results = search_similar_chunks(query, index, chunks)
        
        prompt_response = "\n".join([
            "다음 문단을 참고하여 질문에 답해주세요:\n",
            *[f"- {chunk}" for chunk in results],
            f"\n질문: {query}"
        ])
        #print("반환 타입 확인:", type(prompt_response))
        return prompt_response
    
    except Exception as e:
        print("Tool 실행 중 오류 발생:", e)
        traceback.print_exc()
        return "오류 발생: 파일을 찾을 수 없습니다."

if __name__ == "__main__":
    mcp.run()
