import csv
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import random

class Data_Object:

    log_ = []

    x_data_ = []
    y_data_ = []

    correction_ = 0.2
    
    used_data_ = []

    def load_data(self, lines, side_images):

        # Placeholders
        images = []
        measurements = []

        # For every line in "lines"...
        for line in lines:

            # Append the center images.
            image_c = cv.imread(line[0])
            images.append(image_c)
            
            # Append the center measurement
            measurement = float(line[3])
            measurements.append(measurement)
            
            if side_images is True:
                
                # Append the side images if requested.
                image_l = cv.imread(line[1])
                image_r = cv.imread(line[2])            
                images.extend((image_l, image_r))            
            
                # Append the side measurements if requested.
                measurements.append(measurement + self.correction_)
                measurements.append(measurement - self.correction_)
           
        # Return a tuple of images and measurements
        return (images, measurements)


    def augment_data(self, images, measurements):

        # Placeholders
        aug_images = []
        aug_measurements = []

        # For every image and measurement...
        for image, measurement in zip(images, measurements):
    
            # Append the original image, and a flipped image.
            aug_images.append(image)
            aug_images.append(cv.flip(image, 1))
    
            # Append the original measurement, and a flipped measurement.
            aug_measurements.append(measurement)
            aug_measurements.append(measurement*-1)
            
        # Return a tuple of augmented images and measurements
        return (aug_images, aug_measurements)

    
    def add_data(self, name, augment=False, side_images=False):
        
        # Check that name isn't already in the "used data" list.
        if name in self.used_data_:
            print ("Object already contains data from this source!")
            return
        
        # Construct the path to the training folder
        path = 'training_data/' + name + '/driving_log.csv'

        # Read the CSV into "lines"
        lines = []
        with open(path) as f:   
            reader = csv.reader(f)
    
            for line in reader:        
                lines.append(line)        

        # Load the data
        images, measurements = self.load_data(lines, side_images)
        
        # Augment the data if requested
        if augment is True:
            images, measurements = self.augment_data(images, measurements)
        
        # Add the new data to the existing data
        self.x_data_ += images
        self.y_data_ += measurements
        
        # Add this data folder to the "used data" list.
        self.used_data_.append(name)
        
        # Construct the log message
        parse_augmented = ""
        if augment is True:
            parse_augmented = "augmented "
            
        parse_side_images = "."
        if side_images is True:
            parse_side_images = " with side images. "
            
        message = "Using " + parse_augmented + "{} data".format(name) + parse_side_images

        self.log_.append(message)
        
        return
    
    
    def print_log(self):
        
        print ()
        
        for message in self.log_:
            print(message)
            
        # Print a few more helpful messages
        print ("There are {} images in the data.".format(len(self.x_data_)))
            
            
    def visualise_data(self):
        
        # Load a random image
        index = random.randint(0, len(self.x_data_))
        image = self.x_data_[index]

        # Convert from BGR to RGB (funny openCV quirk)
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        print (self.y_data_[index])
        plt.imshow(image)
        
        
    def add_model(self, model):
        self.log_.append("Using {} network.".format(model))
        
    
    def get_x_data(self):
        x_data = np.array(self.x_data_)
        return x_data
    
    
    def get_y_data(self):
        y_data = np.array(self.y_data_)
        return y_data    
    
