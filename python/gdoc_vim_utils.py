import os


def do_write(vim, query):
    target_file_path = vim.eval("expand('%:p')")
    target_file_name = vim.eval("expand('%:t')")

    if not target_file_path:
        return -1

    with open(target_file_path, "r") as file:
        file_contents = file.read()

    create_blob = {"title": target_file_name}
    edit_blob = [
        {
            "insertText": {
                "location": {
                    "index": 1,
                },
                "text": file_contents,
            }
        }
    ]

    doc = query.create_doc(create_blob)

    if doc["id"] != None:
        print(
            '[gdoc.vim] Created a document with the id "%s" and title "%s" '
            % (doc["id"], doc["title"])
        )

        query.write_id_to_file(doc["id"], target_file_path)
        print("[gdoc.vim] Saved the document ID to %s" % query.gdoc_file)

        if query.edit_doc(doc["id"], edit_blob):
            print(
                "[gdoc.vim] Successfully written the document with the id %s"
                % doc["id"]
            )
    else:
        return -2


def doc_write(vim, query, GdocErr):
    target_file_path = vim.eval("expand('%:p')")
    target_file_name = vim.eval("expand('%:t')")

    if (
        os.path.exists(query.gdoc_file)
        and query.open_doc_from_file(fname=target_file_path, idx="") != -1
    ):
        print(
            '[gdoc.vim] Document "%s" already exists in google docs.' % target_file_name
        )
    else:
        i = do_write(vim, query)
        if i == -1:
            raise GdocErr("[gdoc.vim] Empty buffer, no text to write.")
        elif i == -2:
            raise GdocErr("[gdoc.vim] Something went wrong.")


def doc_fetch(vim, query, GdocErr):
    document_id = vim.eval("a:doc_id")

    try:
        content = query.read_doc(document_id)
    except:
        raise GdocErr(
            f"Was unable to read document of id '{document_id}' perhaps its invalid?"
        )

    extracted_text = query.parse_doc(content)[0]
    lines = extracted_text.split("\n")

    for line_number, line_content in enumerate(lines):
        vim.command(f"call setline({line_number + 1}, '{line_content}')")

    vim.command("write!")

    target_file_path = vim.eval("expand('%:p')")

    query.write_id_to_file(document_id, target_file_path)

    print(f"gdoc.vim: local association created for {document_id}")


def doc_sync_doc(vim, query, GdocErr):
    target_file_name = vim.eval("expand('%:t')")
    target_file_path = vim.eval("expand('%:p')")
    document = query.open_doc_from_file(target_file_path)

    if document != -1:
        remote_doc_content = document[0][0]
        local_file = document[2]

        with open(local_file, "w") as file:
            file.write(remote_doc_content)

        print("[gdoc.vim] Successfully synced remote doc to local file")
    else:
        raise GdocErr(
            'Document "%s" is not synced with google docs yet, try running :Gdoc write'
            % target_file_name
        )


def doc_sync(vim, query, GdocErr):
    target_file_name = vim.eval("expand('%:t')")
    target_file_path = vim.eval("expand('%:p')")

    if (
        os.path.exists(query.gdoc_file)
        and query.open_doc_from_file(fname=target_file_path, idx="") != -1
    ):
        print("[gdoc.vim] Syncing document...")
        id = query.open_doc_from_file(fname=target_file_path, idx="")[1]

        with open(target_file_path) as file:
            new_content = file.read()

        if query.sync_doc(new_content, id) != -1:
            print("[gdoc.vim] Successfully synced the local file to remote doc")

        else:
            raise GdocErr("Something went wrong")

    else:
        raise GdocErr(
            'Document "%s" is not synced with google docs yet, try running :Gdoc write\''
            % target_file_name
        )


def doc_rm(vim, query, GdocErr):
    target_file_name = vim.eval("expand('%:t')")
    target_file_path = vim.eval("expand('%:p')")
    local_doc = query.open_doc_from_file(target_file_path)

    if local_doc != -1:
        file_id = local_doc[1]
        line = local_doc[3]

        dq = query.delete_doc(file_id)
        if dq[0] == 0:
            query.delete_line_from_file(line)
            print(
                '[gdoc.vim] Successfully deleted "%s" from google docs'
                % target_file_name
            )
        else:
            raise GdocErr("Something went wrong")
    else:
        raise GdocErr(
            'Document "%s" is not synced with google docs yet, try running :Gdoc write'
            % target_file_name
        )
