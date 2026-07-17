def reflect_response(
    tools: list,
    result,
):
    """
    Validates tool execution and determines whether
    additional user input is required.
    """

    if result is None:

        return {
            "success": False,
            "message": "No response was generated.",
            "needs_followup": False,
            "followup_question": None
        }

    if isinstance(result, str):

        result = result.strip()

        if len(result) == 0:

            return {
                "success": False,
                "message": "Generated response is empty.",
                "needs_followup": False,
                "followup_question": None
            }

    if (
        "knowledge_search" in tools
        and isinstance(result, str)
        and "not found in the uploaded documents" in result.lower()
    ):

        return {

            "success": True,

            "message": "Knowledge search completed.",

            "needs_followup": False,

            "followup_question": None

        }

    if "leave_application" in tools:

        lower = result.lower()

        if (
            "reason" not in lower
            and "medical" not in lower
        ):

            return {

                "success": True,

                "message": "Leave application generated.",

                "needs_followup": False,

                "followup_question": None

            }

    return {

        "success": True,

        "message": "Execution completed successfully.",

        "needs_followup": False,

        "followup_question": None

    }