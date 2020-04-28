import thulac
from py2neo import Graph,Node,Relationship,NodeMatcher


# print(cut_text)
entity_dict = {}
entity_type_dict = {}
def init():
    with open("entity.txt","r",encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip('\n')
            line = line.split('\t')
            entity_dict[line[1]] = line[0]

    with open("entity_type.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip('\n')
            line = line.split(' ')
            entity_type_dict[line[0]] = line[1]

def analyse_question(text,cutter):
    cut_text = cutter.cut(text)
    entity_list = []
    entity_type_list = []
    for seg in cut_text:
        if seg[0] in entity_type_dict.keys():
            entity_type_list.append(seg[0])
        elif seg[0] in entity_dict.keys():
            entity_list.append(seg[0])
    # print(cut_text)
    # print(entity_list)
    # print(entity_type_list)
    graph = Graph("http://localhost:7474", username="", password='')
    for entity in entity_list:
        for entity_type in entity_type_list:
            # print("MATCH (entity1) - [rel] - (entity2:%s)  WHERE entity1.name ='%s' RETURN entity2.name"%(entity_type_dict[entity_type],entity))
            ans = graph.run("MATCH (entity1) - [rel] - (entity2:%s)  WHERE entity1.name ='%s' RETURN entity2.name"%(entity_type_dict[entity_type],entity)).data()
            if len(ans) is not 0:
                response = "%s相关的%s有:"%(entity,entity_type)
                # print(ans)
                for dict in ans:
                    response += dict['entity2.name'] + ","
                response = response[:-1]
                print(response)
            else:
                response = "%s相关的%s暂未有了解，我们会继续完善补充数据的！(≧∀≦)ゞ"%(entity,entity_type)
                print(response)
        if len(entity_type_list) == 0:
            response = "您所提问%s的相关内容我们暂不了解，我们会继续完善补充数据的！(≧∀≦)ゞ"%(entity)
            print(response)
    if len(entity_list) == 0:
        response = "您所提问的我们暂不了解，我们会继续完善补充数据的！(≧∀≦)ゞ"
        print(response)

if __name__ == "__main__":
    init()
    # text = "我想了解苏州瑞博公司的研究平台"
    cutter = thulac.thulac(user_dict="user_dict.txt")
    while True:
        text = input('TechBot请您提问...>>')
        analyse_question(text,cutter=cutter)
