

def ternaryImg(equalizedImg, noisyPercentile):
    
    # noisyPercentile = 20 
    p5a = np.percentile(equalizedImage, noisyPercentile);

    rowCount=0;
    colCount=0;
    noiseCount=0;
    topCount=0;
    botCount=0;
    for row in equalizedImage:
        for pixel in row:
            if pixel<p5a:
                ternImage[rowCount][colCount]=128;
                noiseCount+=1;
            elif pixel>0.6:
                ternImage[rowCount][colCount]=255;
                topCount+=1;
            else:
                ternImage[rowCount][colCount]=0;
                botCount+=1;
            colCount+=1;
        colCount=0;
        rowCount+=1;
    
    return ternImage




def generateIrisCode(ternImage):
     
    # step 5: divide the image into tiles
    # 49 pixels per segment: 10 row
    # 10 pixels: 5 col 
    
    M=49
    N=10
    # moves left to right and then top to bottom
    tiles = [ternImage[x:x+M,y:y+N] for x in range(0,ternImage.shape[0],M) for y in range(0,ternImage.shape[1],N)]; 
    
    
    # step 6: generate a single bit for each tile
    # alternative: generate a 2 bit? 3bit? per tile
    # create a bit mask
    # idea 1
    bitMask=np.zeros((50));
    irisCode=np.zeros((50));
    
    white=0;
    black=0;
    noise=0;
    unaccounted=0;
    irisCodeIndex=0;
    for tile in tiles:
        for row in tile:
            for pixel in row:
                #print(pixel)
                if pixel==255:
                    white+=1;
                elif pixel==0:
                    black+=1;
                elif pixel==128:
                    noise+=1;
                else:
                    print("unaccoutned at tile number: "+str(irisCodeIndex)+" pixel value: "+str(pixel));
        if white>black:
            irisCode[irisCodeIndex]=1;
        else:
            irisCode[irisCodeIndex]=0;
        if noise>0:
            bitMask[irisCodeIndex]=0;
        else:
            bitMask[irisCodeIndex]=1;
        white=0;
        black=0;
        noise=0;
        unaccounted=0;
        irisCodeIndex+=1;
    
    return (irisCode, bitMask)