import invoke

def do_check_dataset_registry():
    the_ctx = invoke.context.Context()
    res = the_ctx.run("ls /")
    stdout_txt = res.stdout
    print("\n"+"="*20+"\n"+"stdout = %s\n" % stdout_txt)
