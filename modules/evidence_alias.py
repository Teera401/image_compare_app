class EvidenceAlias:
    def __init__(self):
        self.ref_alias = None
        self.evd_alias_list = list()
        self.group = None
        self.alias_membergroup_ls:list = None #list of EvidenceAlias

    def haveGroup(self):
        return self.group != None and len(self.group) > 0
        
    def add_evdalias_list(self, evdalias):
        self.evd_alias_list.append(evdalias)

    def iscompitible_refalias(self, refalias):
        for evdalias in self.evd_alias_list :
             if evdalias == refalias:
                 return True
        return False