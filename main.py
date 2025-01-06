import boto3

def delete_all_open_sessions():
    client = boto3.client('ssm')

    # セッションの一覧を取得
    open_sessions = []
    next_token = None
    while True:
        if next_token:
            response = client.describe_sessions(
                State='Active',
                NextToken=next_token
            )
        else:
            response = client.describe_sessions(
                State='Active'
            )

        open_sessions.extend(response['Sessions'])
        next_token = response.get('NextToken')
        if not next_token:
            break

    # オープンになっているセッションを削除
    for session in open_sessions:
        session_id = session['SessionId']
        try:
            client.terminate_session(SessionId=session_id)
            print(f"Session {session_id} terminated successfully.")
        except Exception as e:
            print(f"Failed to terminate session {session_id}: {e}")

if __name__ == "__main__":
    delete_all_open_sessions()

