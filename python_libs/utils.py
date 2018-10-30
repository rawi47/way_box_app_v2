
def _create_file(source,content,right):
    file = open(source,right)
    file.write(content)
    file.close()
