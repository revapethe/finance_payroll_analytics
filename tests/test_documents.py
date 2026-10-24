import pytest

pytest.importorskip("chromadb")
from app import documents
from etl import index_documents


def test_index_build_repeat_and_retrieve(tmp_path, monkeypatch):
    destination = tmp_path / "chroma"
    monkeypatch.setattr(documents, "INDEX", destination)
    monkeypatch.setattr(index_documents, "INDEX", destination)
    files, chunks = index_documents.build_index()
    assert files == 25 and chunks >= files
    assert index_documents.build_index() == (files, chunks)
    index = documents.open_index()
    result = index.query(["remote work policy"])
    assert len(result["documents"][0]) == 3
    assert any("Remote_Work" in meta["filename"] for meta in result["metadatas"][0])
    assert index.count() == chunks


def test_absent_index_is_optional(tmp_path, monkeypatch):
    monkeypatch.setattr(documents, "INDEX", tmp_path / "missing")
    assert documents.open_index() is None
