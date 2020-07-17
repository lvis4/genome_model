#!/usr/bin/env python
# coding: utf-8

# In[2]:


import cobra
import pandas as pd


# In[3]:


model = cobra.io.read_sbml_model("GSMGb_model.sbml")


# In[83]:


model.summary()


# In[3]:


cpd = pd.read_excel("compounds.xls")


# In[4]:


cpd.head()


# In[4]:


rcn = pd.read_excel("reactions.xls")


# In[6]:


rcn.head()


#     TO CHECK THE REVERSIBILITY OF THE REACTIONS IN THE MODEL WITH THE DATABASE

# In[18]:


count =0 #to count the number of reactions modified in the model.reactions

#this loops takes some time to run, kindly be patient
for i in model.reactions:
    if i.id[0]== 'r':
        tmp = i.id[0:8]
        for t in range(len(rcn['DATABASE'])):
            if tmp==rcn.loc[t,'DATABASE']:
                if rcn.loc[t,'THERMODYNAMIC FEASIBILTY'] == '<=>':
                    if i.lower_bound !=-1000.0 or i.upper_bound!=1000.0:
                        count+=1
                        i.lower_bound = -1000.0
                        i.upper_bound = 1000.0
                elif tmp == rcn.loc[t,'THERMODYNAMIC FEASIBILTY'] == "<=":
                    if i.lower_bound != -1000.0 or i.upper_bound!=0.0:
                        i.lower_bound = -1000.0
                        i.upper_bound = 0.0
                        count+=1
                elif tmp == rcn.loc[t,'THERMODYNAMIC FEASIBILTY'] == "=>":
                    if i.lower_bound!=0.0 or i.upper_bound!=-1000.0:
                        i.lower_bound = 0.0
                        i.upper_bound = 1000.0
                        count+=1
print("Job finished")


# In[20]:


count #the reaction bounds were apparently fine 


# In[24]:


model.metabolites.cpd00027_c0.summary()


# In[11]:


model.metabolites.cpd00027_c0


#     TO CHECK THE FORMULA OF THE COUMPOUNDS IN THE MODEL AND REPLACE THEM WITH THE DATABASE

# In[25]:


for i in model.metabolites:
    for t in range(len(cpd['DATABASE'])):
        if i.id[0:8]==cpd.loc[t,'DATABASE']:
            i.formula = cpd.loc[t,'FORMULA']
print('Job Finished')


# In[26]:


model.metabolites.cpd02375_c0


# In[31]:


model.metabolites.cpd00027_c0.charge


#     TO CHECK THE CHARGE OF THE COMPOUNDS AND REPLACE IT WITH THE DATABASE

# In[29]:


cnter =0 #To count the number of compounds with different charges 

#this loop takes some time to run, kindly be patient 
for i in model.metabolites:
    for t in range(len(cpd['DATABASE'])):
        if i.id[0:8]==cpd.loc[t,'DATABASE']:
            if i.charge != cpd.loc[t,'CHARGE']:
                i.charge = cpd.loc[t,'CHARGE']
                cnter+=1
            
print('Job Finished')


# In[32]:


cnter # number of metabolites changed 


# In[23]:


cpd.loc[2328,]


# In[4]:


medium = model.medium


# In[55]:


medium['EX_cpd00027_b']


# In[54]:


for i in model.medium:
    print(i[3:11])


# In[59]:


media = list()

#TO FIND OUT THE LIST OF COMPOUNDS IN THE MEDIA
for i in model.medium:
    for t in range(len(cpd['DATABASE'])):
        if i[3:11]==cpd.loc[t,'DATABASE']:
            media.append(cpd.loc[t,'PRIMARY NAME'])


# In[91]:


j=0
for i in model.medium.items():
    print(i[0],'\t','%s' % media[j],'\t\t',i[1])
    j+=1


# In[98]:


medium['EX_cpd00027_b'] =1000.0


# In[6]:


media2 = list()
for i in model.medium:
    if i =='EX_cpd00027_b':
        continue
    else:
        medium[i] =0


# In[7]:


model.medium = medium


# In[8]:


model.medium


# In[9]:


model.slim_optimize()


# In[10]:


model.summary()


# In[ ]:




