class AACStaticTables():

	ff_aac_num_swb_1024= [41, 41, 47, 49, 49, 51, 47, 47, 43, 43, 43, 40, 40]
	'''
	ff_aac_num_swb_512= [0, 0, 0, 36, 36, 37, 31, 31, 0, 0, 0, 0, 0]
	ff_aac_num_swb_480= [0, 0, 0, 35, 35, 37, 30, 30, 0, 0, 0, 0, 0]
	'''
	ff_aac_num_swb_128= [12, 12, 12, 14, 14, 14, 15, 15, 15, 15, 15, 15, 15]

	ff_tns_max_bands_1024= [31, 31, 34, 40, 42, 51, 46, 46, 42, 42, 42, 39, 39]
	'''
	ff_tns_max_bands_512= [0, 0, 0, 31, 32, 37, 31, 31, 0, 0, 0, 0, 0]
	ff_tns_max_bands_480= [0, 0, 0, 31, 32, 37, 30, 30, 0, 0, 0, 0, 0]
	'''
	ff_tns_max_bands_128= [9, 9, 10, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14]




	swb_offset_1024_96= [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 64, 72, 80, 88, 96, 108, 120, 132, 144, 156, 172, 188, 212, 240, 276, 320, 384, 448, 512, 576, 640, 704, 768, 832, 896, 960, 1024]
	swb_offset_1024_64= [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 64, 72, 80, 88, 100, 112, 124, 140, 156, 172, 192, 216, 240, 268, 304, 344, 384, 424, 464, 504, 544, 584, 624, 664, 704, 744, 784, 824, 864, 904, 944, 984, 1024]
	swb_offset_1024_48= [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 48, 56, 64, 72, 80, 88, 96, 108, 120, 132, 144, 160, 176, 196, 216, 240, 264, 292, 320, 352, 384, 416, 448, 480, 512, 544, 576, 608, 640, 672, 704, 736, 768, 800, 832, 864, 896, 928, 1024]
	swb_offset_1024_32= [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 48, 56, 64, 72, 80, 88, 96, 108, 120, 132, 144, 160, 176, 196, 216, 240, 264, 292, 320, 352, 384, 416, 448, 480, 512, 544, 576, 608, 640, 672, 704, 736, 768, 800, 832, 864, 896, 928, 960, 992, 1024]
	swb_offset_1024_24= [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 52, 60, 68, 76, 84, 92, 100, 108, 116, 124, 136, 148, 160, 172, 188, 204, 220, 240, 260, 284, 308, 336, 364, 396, 432, 468, 508, 552, 600, 652, 704, 768, 832, 896, 960, 1024]
	swb_offset_1024_16= [0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 100, 112, 124, 136, 148, 160, 172, 184, 196, 212, 228, 244, 260, 280, 300, 320, 344, 368, 396, 424, 456, 492, 532, 572, 616, 664, 716, 772, 832, 896, 960, 1024]
	swb_offset_1024_8= [0, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120, 132, 144, 156, 172, 188, 204, 220, 236, 252, 268, 288, 308, 328, 348, 372, 396, 420, 448, 476, 508, 544, 580, 620, 664, 712, 764, 820, 880, 944, 1024]

	'''
	swb_offset_512_48= [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 68, 76, 84, 92, 100, 112, 124, 136, 148, 164, 184, 208, 236, 268, 300, 332, 364, 396, 428, 460, 512]
	swb_offset_512_32= [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 64, 72, 80, 88, 96, 108, 120, 132, 144, 160, 176, 192, 212, 236, 260, 288, 320, 352, 384, 416, 448, 480, 512]
	swb_offset_512_24= [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 52, 60, 68, 80, 92, 104, 120, 140, 164, 192, 224, 256, 288, 320, 352, 384, 416, 448, 480, 512, 	]

	swb_offset_480_48= [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 64, 72, 80, 88, 96, 108, 120, 132, 144, 156, 172, 188, 212, 240, 272, 304, 336, 368, 400, 432, 480]
	swb_offset_480_32= [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 72, 80, 88, 96, 104, 112, 124, 136, 148, 164, 180, 200, 224, 256, 288, 320, 352, 384, 416, 448, 480]
	swb_offset_480_24= [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 52, 60, 68, 80, 92, 104, 120, 140, 164, 192, 224, 256, 288, 320, 352, 384, 416, 448, 480]
	'''

	swb_offset_128_96= [0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 92, 128]
	swb_offset_128_48= [0, 4, 8, 12, 16, 20, 28, 36, 44, 56, 68, 80, 96, 112, 128]
	swb_offset_128_24= [0, 4, 8, 12, 16, 20, 24, 28, 36, 44, 52, 64, 76, 92, 108, 128]
	swb_offset_128_16= [0, 4, 8, 12, 16, 20, 24, 28, 32, 40, 48, 60, 72, 88, 108, 128]
	swb_offset_128_8= [0, 4, 8, 12, 16, 20, 24, 28, 36, 44, 52, 60, 72, 88, 108, 128]

	ff_swb_offset_1024= [
		swb_offset_1024_96, swb_offset_1024_96, swb_offset_1024_64,
		swb_offset_1024_48, swb_offset_1024_48, swb_offset_1024_32,
		swb_offset_1024_24, swb_offset_1024_24, swb_offset_1024_16,
		swb_offset_1024_16, swb_offset_1024_16, swb_offset_1024_8,
		swb_offset_1024_8
	]
 
	'''
	ff_swb_offset_512= [
		False,				False,				False,	
		swb_offset_512_48,	swb_offset_512_48,	swb_offset_512_32,	
		swb_offset_512_24,	swb_offset_512_24,	False,	
		False,				False,				False,	
		False
	]
 
	ff_swb_offset_480= [
		False,				False,				False,	
		swb_offset_480_48,	swb_offset_480_48,	swb_offset_480_32,	
		swb_offset_480_24,	swb_offset_480_24,	False,	
		False,				False,				False,	
		False
	]
 	'''

	ff_swb_offset_128= [
		swb_offset_128_96, swb_offset_128_96, swb_offset_128_96,
		swb_offset_128_48, swb_offset_128_48, swb_offset_128_48,
		swb_offset_128_24, swb_offset_128_24, swb_offset_128_16,
		swb_offset_128_16, swb_offset_128_16, swb_offset_128_8,
		swb_offset_128_8
	]
 




	ff_aac_pred_sfb_max= [33, 33, 38, 40, 40, 40, 41, 41, 37, 37, 37, 34, 34]

	ff_aac_scalefactor_code= [
		0x3ffe8, 0x3ffe6, 0x3ffe7, 0x3ffe5, 0x7fff5, 0x7fff1, 0x7ffed, 0x7fff6,
		0x7ffee, 0x7ffef, 0x7fff0, 0x7fffc, 0x7fffd, 0x7ffff, 0x7fffe, 0x7fff7,
		0x7fff8, 0x7fffb, 0x7fff9, 0x3ffe4, 0x7fffa, 0x3ffe3, 0x1ffef, 0x1fff0,
		0x0fff5, 0x1ffee, 0x0fff2, 0x0fff3, 0x0fff4, 0x0fff1, 0x07ff6, 0x07ff7,
		0x03ff9, 0x03ff5, 0x03ff7, 0x03ff3, 0x03ff6, 0x03ff2, 0x01ff7, 0x01ff5,
		0x00ff9, 0x00ff7, 0x00ff6, 0x007f9, 0x00ff4, 0x007f8, 0x003f9, 0x003f7,
		0x003f5, 0x001f8, 0x001f7, 0x000fa, 0x000f8, 0x000f6, 0x00079, 0x0003a,
		0x00038, 0x0001a, 0x0000b, 0x00004, 0x00000, 0x0000a, 0x0000c, 0x0001b,
		0x00039, 0x0003b, 0x00078, 0x0007a, 0x000f7, 0x000f9, 0x001f6, 0x001f9,
		0x003f4, 0x003f6, 0x003f8, 0x007f5, 0x007f4, 0x007f6, 0x007f7, 0x00ff5,
		0x00ff8, 0x01ff4, 0x01ff6, 0x01ff8, 0x03ff8, 0x03ff4, 0x0fff0, 0x07ff4,
		0x0fff6, 0x07ff5, 0x3ffe2, 0x7ffd9, 0x7ffda, 0x7ffdb, 0x7ffdc, 0x7ffdd,
		0x7ffde, 0x7ffd8, 0x7ffd2, 0x7ffd3, 0x7ffd4, 0x7ffd5, 0x7ffd6, 0x7fff2,
		0x7ffdf, 0x7ffe7, 0x7ffe8, 0x7ffe9, 0x7ffea, 0x7ffeb, 0x7ffe6, 0x7ffe0,
		0x7ffe1, 0x7ffe2, 0x7ffe3, 0x7ffe4, 0x7ffe5, 0x7ffd7, 0x7ffec, 0x7fff4,
		0x7fff3
	]

	ff_aac_scalefactor_bits= [
		18, 18, 18, 18, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
		19, 19, 19, 18, 19, 18, 17, 17, 16, 17, 16, 16, 16, 16, 15, 15,
		14, 14, 14, 14, 14, 14, 13, 13, 12, 12, 12, 11, 12, 11, 10, 10,
		10,  9,  9,  8,  8,  8,  7,  6,  6,  5,  4,  3,  1,  4,  4,  5,
		 6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 10, 11, 11, 11, 11, 12,
		12, 13, 13, 13, 14, 14, 16, 15, 16, 15, 18, 19, 19, 19, 19, 19,
		19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
		19, 19, 19, 19, 19, 19, 19, 19, 19
	]
