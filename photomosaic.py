from PIL import Image#,ImageFilter
import numpy as np
import glob
import math

def load_image(filepath):
    try:
        input_image=Image.open(filepath)
        width=input_image.size[0]
        height=input_image.size[1]
        print("The width x height is: ",width," x ",height)
        resized_image=input_image
        resized_image.thumbnail((2000,2000))
        resized_width=resized_image.size[0]
        resized_height=resized_image.size[1]
        print("The resized width x height is: ",resized_width," x ",resized_height)
        #input_image.save("resized_test.jpg")
        #input_image.filter(ImageFilter.BLUR)
        #input_image.save("filtered_test.jpg")
        return (resized_image,min(resized_width,resized_height))
    except:
        print("Image unable to load")

def split_image(input_image,n_pixel):
    pixel_matrix=np.array(input_image)
    #print(pixel_matrix)
    n_rows=int(input_image.size[1]/n_pixel)
    n_columns=int(input_image.size[0]/n_pixel)
    
    average_pixel_matrix=np.zeros((n_rows,n_columns,3),dtype=int)
    
    for i in range(0,input_image.size[1]-n_pixel,n_pixel):
        for j in range(0,input_image.size[0]-n_pixel,n_pixel):
            
            r_sum=0
            g_sum=0
            b_sum=0

            for k in range(n_pixel):
                for l in range(n_pixel):        
                    r_sum+=pixel_matrix[i+k,j+l][0]
                    g_sum+=pixel_matrix[i+k,j+l][1]
                    b_sum+=pixel_matrix[i+k,j+l][2]

                    
            average_pixel_matrix[int(i/n_pixel),int(j/n_pixel)]=(int(r_sum/(n_pixel*n_pixel)),int(g_sum/(n_pixel*n_pixel)),int(b_sum/(n_pixel*n_pixel)))
            
    return average_pixel_matrix
        
def pixelate(pixel_matrix,name):
    average_pixel_image=Image.fromarray(np.uint8(pixel_matrix))
    average_pixel_image.save(name)
    average_pixel_image.show()
                  
def crop_image_list(source_filepath,destination_filepath,crop_image_size):
    count=1
    for filename in glob.glob(source_filepath+"\*.jpg"):
        im=Image.open(filename)
        width,height=im.size
        if count!=600:
            left=(width-min(width,height))/2
            top = (height-min(width,height))/2
            right = (width+min(width,height))/2
            bottom = (height+min(width,height))/2
            im=im.crop((left,top,right,bottom))
            im.thumbnail((crop_image_size,crop_image_size))
            im.save(destination_filepath+"\crop_image"+str(count)+".jpg")
            count+=1
        elif count==600:
            break
    return   
    
def average_colour(filepath):
    im=Image.open(filepath)
    pixel_matrix=np.array(im)    
    row=pixel_matrix.shape[0]
    column=pixel_matrix.shape[1]
    r_sum=0
    g_sum=0
    b_sum=0
    for i in range(row):
        for j in range(column):
            r_sum+=pixel_matrix[i,j,0]
            g_sum+=pixel_matrix[i,j,1]
            b_sum+=pixel_matrix[i,j,2]
    average_colour=(int(r_sum/(row*column)),int(g_sum/(row*column)),int(b_sum/(row*column)))
    return average_colour    

def eucledian_distance(pixel_one,pixel_two):
    return (math.sqrt((math.pow((pixel_two[0]-pixel_one[0]),2))+(math.pow((pixel_two[1]-pixel_one[1]),2))+(math.pow((pixel_two[2]-pixel_one[2]),2))))



print("Loading original image to be photomosaiked")    
(original_image,min_size)=load_image("test.jpg")

print("Extracting average pixel colour from original image")
pixel_matrix=split_image(original_image,10)

#print("Creating average pixel image")
#pixelate(pixel_matrix,"average_pixel_test.jpg")

crop_image_size=250
print("Cropping source images")
source_filepath="Source Images"
destination_filepath="Cropped Images"
crop_image_list(source_filepath,destination_filepath,crop_image_size)

print("Calculating average colour of cropped source images")
average_colour_list=[]
for filename in glob.glob(destination_filepath+"\*.jpg"):
    average_colour_list.append(average_colour(filename))
#print(average_colour_list)

image_index=np.zeros((pixel_matrix.shape[0],pixel_matrix.shape[1]),dtype=int)
for i in range(pixel_matrix.shape[0]):
    for j in range(pixel_matrix.shape[1]):
        pixel_difference=[]
        for k in range(len(average_colour_list)):
            pixel_difference.append(eucledian_distance(pixel_matrix[i][j],average_colour_list[k]))
        image_index[i][j]=((pixel_difference.index(min(pixel_difference)))+1)
#print(image_index)

print("Creating collage image")
collage_image_matrix=255*np.ones((crop_image_size*image_index.shape[0],crop_image_size*image_index.shape[1],3),np.uint8)
collage_image=Image.fromarray(np.uint8(collage_image_matrix))
for j in range(image_index.shape[1]):
    for i in range(image_index.shape[0]):
        similiar_colour_image=Image.open(destination_filepath+"\crop_image"+str(image_index[i][j])+".jpg")
        collage_image.paste(similiar_colour_image,(j*crop_image_size,i*crop_image_size))
        
collage_image.thumbnail((30000,30000))
collage_image.save("collage_image.png")
collage_image.show()