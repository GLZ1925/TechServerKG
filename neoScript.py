from py2neo import Graph

def scriptToNeo():
    # 链接知识图谱，注意写上自己neo4j图数据库的用户名和密码
    graph = Graph("http://localhost:7474", username="", password='')
    # 根据cypher语法把我们要放入的实体和关系脚本创建好
    create_entity_order = []
    entity_label = {}
    with open('小核酸实体.txt', 'r', encoding='UTF-8') as f:
        for line in f.readlines():
            count = 0
            for value in line.split('\t'):
                if count % 2 == 0:
                    label = value
                else:
                    entity = value
                    entity = entity.replace('\n', '')
                count += 1
            # print('label:',label)
            # print('entity:',entity)
            order = "create (n:%s {name:'%s'}) " % (label, entity)
            entity_label[entity] = label
            print(order)
            create_entity_order.append(order)
    relation_type = {
        'concurrency': '概念上相关',
        'close_to': '概念上相关',
        'rely_on': '概念上相关',
        'derive': '概念上相关',
        'subclass': '概念上相关',
        'cover': '概念上相关',
        'synonymous': '概念上相关',
        'produce': '物理上相关',
        'develop': '物理上相关',
        'belong': '物理上相关',
        'own': '物理上相关',
        'cooperate': '物理上相关',
        'degradate': '物理上相关',
        'build': '物理上相关',
        'apply_to': '功能上相关',
        'act_on': '功能上相关',
        'induce': '功能上相关',
        'restrain': '功能上相关',
        'focus_on': '功能上相关'
    }
    with open('小核酸关系.txt', 'r', encoding='UTF-8') as f:
        for line in f.readlines():
            count = 0
            for value in line.split('\t'):
                if count % 3 == 0:
                    entity1 = value
                elif count % 3 == 1:
                    relation = value
                    relation = relation.replace('\n', '')
                    relation_label = relation_type[relation]
                elif count % 3 == 2:
                    entity2 = value
                    entity2 = entity2.replace('\n', '')
                count += 1
            order = "match (entity1:%s) ,(entity2:%s) where entity1.name = '%s' and entity2.name = '%s' create (entity1)-[r:%s {name:'%s'}]->(entity2)" \
                    % (entity_label[entity1], entity_label[entity2], entity1, entity2, relation_label, relation)
            print(order)

    create_relation_order = []
    create_relation_order.append(order)

    # 执行命令存入neo4j数据库
    for order in create_entity_order:
        graph.run(order)
    for order in create_relation_order:
        graph.run(order)

if __name__ == "__main__":
    scriptToNeo()
