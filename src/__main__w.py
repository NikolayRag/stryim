import stryim
import args



if __name__ == '__main__':
	cArgs= args.parse(True)

	if cArgs:
		stryim.start(True, cArgs.dst, cArgs.nonstop)


