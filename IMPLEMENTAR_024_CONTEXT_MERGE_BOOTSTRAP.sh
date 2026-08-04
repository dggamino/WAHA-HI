#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMPLEMENTAR 024 — Conversation Memory + Knowledge Context Merge Foundation v0.1.0 ==="


mkdir -p companion/context


touch companion/context/__init__.py


cat > companion/context/__init__.py <<'EOF'
"""
Conversation Context Layer
"""
EOF


cat > companion/context/models.py <<'EOF'
from dataclasses import dataclass


@dataclass
class ConversationContext:

    session_id: str
    user_id: str
    intent: str = ""
    memory: dict = None
    knowledge: list = None


    def __post_init__(self):

        if self.memory is None:

            self.memory = {}


        if self.knowledge is None:

            self.knowledge = []
EOF


cat > companion/context/merge.py <<'EOF'
"""
Context aggregation layer.
"""


from companion.connectors.knowledge import KnowledgeConnector



class ContextMerger:


    def __init__(self):

        self.knowledge = KnowledgeConnector()



    def build(
        self,
        session,
        intent,
        query
    ):


        knowledge_result = self.knowledge.query(
            query
        )


        return {

            "session":

            {

                "id":
                session.session_id,

                "user":
                session.user_id

            },


            "intent":
            intent,


            "memory":
            session.state,


            "knowledge":
            knowledge_result["results"]

        }
EOF


cat > companion/context/service.py <<'EOF'
"""
Conversation Context Service.
"""


from companion.context.merge import ContextMerger



class ContextService:


    def __init__(self):

        self.merger = ContextMerger()



    def create_context(
        self,
        session,
        intent,
        query
    ):

        return self.merger.build(

            session,

            intent,

            query

        )
EOF


cat > companion/context/README.md <<'EOF'
# Conversation Context Merge

Une:

- Session state.
- Intent.
- Knowledge retrieval.

No contiene:

- CRM.
- WhatsApp.
- Editorial content.
EOF


echo ""
echo "=== VALIDACION CONTEXT MERGE ==="

python3 - <<'EOF'

from sessions.service import SessionService
from companion.context.service import ContextService


sessions = SessionService()


session = sessions.create(
    "5210000000000"
)


sessions.update_state(
    session.session_id,
    "topic",
    "hereditaria"
)


service = ContextService()


context = service.create_context(

    session,

    "book_interest",

    "Cuidador"

)


print(context)


EOF


echo ""
echo "=== IMPLEMENTAR 024 COMPLETADO ==="
