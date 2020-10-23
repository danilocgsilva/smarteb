# smarteb
Smart Elasticbeanstalk - web stack managed in an trully easy way

## Usage

First, you need to install. Just go to the repository home and type:
```
pip install . --user
```

Then the application becomes system wide available. The commands are available through the command line "`smeb`", which stans for *smart elasticbeanstalk*.

**To list the current applications:** 
```
smeb
```
Listing applications is the default behavour.

Same for:
```
smeb list
```

**To create a new application:**

```
smeb new
```

**To delete an application**

```
smeb delete:<your-application-name>
```
** NOTE THAT RIGHT NOW, DELETING AN APPLICATION IS ONLY AVAILABLE FOR ONES THAT STILL DOES NOT HAVE RUNNING ENVIRONMENT. IF IS THE CASE, FIRST NEEDS TO TERMINATE ALL ENVIRONMENTS BEFORE DELETING AND APPLICATION THROUGH SMEB **

**To delete several applications at once**
```
smeb delete:<your-first-application-name>,<second-application-name>,<n-application-name>
```
