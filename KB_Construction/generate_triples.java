
import org.apache.jena.ontology.*;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.Resource;
import org.apache.jena.util.FileManager;

import java.io.*;
import java.util.Iterator;

public class generate_triples {
    public static void main(String[] args) throws IOException {
        String OWL_file = "./data/njukepractice.owl";
        String Output_file = "./data/RDF.owl";
        // 读取OWL文件，建立模型
        OntModel model = ModelFactory.createOntologyModel();
        InputStream ontologyIn = FileManager.get().open(OWL_file);
        try {
            model.read(ontologyIn, "RDF/XML");
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }

        String NS = "http://ws.nju.edu.cn/tcqa#";
        // 建立推理
        OntModel inf = ModelFactory.createOntologyModel(OntModelSpec.OWL_MEM_MICRO_RULE_INF, model);
        // 获取类，一共3个类
        OntClass people = model.getOntClass(NS + "人物");
        OntClass event = model.getOntClass(NS + "事件");
        OntClass regime = model.getOntClass(NS + "势力");
        // 获取属性，一共20个属性，Object属性2个，Datatype属性18个
        ObjectProperty people_regime = model.getObjectProperty(NS+"效忠势力");
        ObjectProperty event_people = model.getObjectProperty(NS+"涉及人物");
        DatatypeProperty people_fictional = model.getDatatypeProperty( NS + "是否虚构" );
        DatatypeProperty people_intro = model.getDatatypeProperty( NS + "介绍" );
        DatatypeProperty people_birthdate = model.getDatatypeProperty( NS + "出生时间" );
        DatatypeProperty people_deathdate = model.getDatatypeProperty( NS + "死亡时间" );
        DatatypeProperty people_act_birthplace = model.getDatatypeProperty(NS+"古代籍贯");
        DatatypeProperty people_now_birthplace = model.getDatatypeProperty(NS+"现代籍贯");
        DatatypeProperty people_name = model.getDatatypeProperty( NS + "姓名" );
        DatatypeProperty people_character = model.getDatatypeProperty( NS + "字" );
        DatatypeProperty people_gender = model.getDatatypeProperty( NS + "性别" );
        DatatypeProperty people_pinyin = model.getDatatypeProperty( NS + "拼音" );
        DatatypeProperty event_hint = model.getDatatypeProperty( NS + "提示" );
        DatatypeProperty event_date = model.getDatatypeProperty( NS + "时间" );
        DatatypeProperty event_chapter = model.getDatatypeProperty( NS + "章节" );
        DatatypeProperty event_occur_place = model.getDatatypeProperty(NS+"发生地点");
        DatatypeProperty event_intro = model.getDatatypeProperty( NS + "简述" );
        DatatypeProperty event_name = model.getDatatypeProperty( NS + "事件名" );
        DatatypeProperty event_history = model.getDatatypeProperty( NS + "历史" );
        DatatypeProperty regime_name = model.getDatatypeProperty( NS + "势力名" );

        // 读取原始person.csv文件
        BufferedReader reader = new BufferedReader(new FileReader("./data/datasets/person.csv"));
        String line;
        while ((line = reader.readLine()) != null) {
            // CSV格式文件为逗号分隔符文件，这里根据逗号切分
            String item[] = line.split(", ");
            // 对每一个item的内容，将属性名和值提取出来
            for (int i = 0; i < item.length; i++) {
                item[i] = item[i].replace("{", "").replace("\'", "").replace(
                        ":", "").replace("}", "");
            }
            // item的长度为10
            String str[];
            str = item[0].split(" ");
            String var[] = str[1].replace("[", " ").replace("]", " ").split(" ");
            if(var.length > 1){
                str[1] = var[0] + "(" + var[1] + ")";
            }
            else{
                str[1] = var[0];
            }
            String name = str[1];
            // 添加一个人物样本
            Individual p = model.createIndividual(NS + name, people);
            for (Iterator<Resource> temp = p.listRDFTypes(true); temp.hasNext(); ) {
                System.out.println(p.getURI() + " is asserted in class " + temp.next());
            }

            // 添加姓名属性
            p.addProperty(people_name, model.createTypedLiteral(name));

            // 添加拼音属性
            str = item[1].split(" ");
            String pinyin = str[1];
            p.addProperty(people_pinyin, model.createTypedLiteral(pinyin));

            // 添加效忠势力属性
            str = item[2].split(" ");
            String s = str[1];
            Resource r = model.createResource(NS + s);
            if(model.containsResource(r)){ //如果效忠势力已有了样本，则直接添加属性
                p.addProperty(people_regime, r);
            }else {
                Individual new_regime = model.createIndividual(NS + s, regime);
                new_regime.addProperty(regime_name, model.createTypedLiteral(s));
                p.addProperty(people_regime, new_regime);
            }

            // 添加性别属性
            str = item[3].split(" ");
            s = str[1];
            p.addProperty(people_gender, model.createTypedLiteral(s));

            // 添加是否虚构属性
            str = item[4].split(" ");
            s = str[1];
            p.addProperty(people_fictional, model.createTypedLiteral(s));

            // 添加字属性
            str = item[5].split(" ");
            s = str[1];
            p.addProperty(people_character, model.createTypedLiteral(s));

            // 添加出生时间属性与死亡时间属性
            str = item[6].split(" ");
            if(str.length < 3){
                p.addProperty(people_birthdate, model.createTypedLiteral("None"));
                p.addProperty(people_deathdate, model.createTypedLiteral("None"));
            }else {
                s = str[1];
                if (s.equals("?")) {
                    p.addProperty(people_birthdate, model.createTypedLiteral("None"));
                }else{
                    p.addProperty(people_birthdate, model.createTypedLiteral(s));
                }
                s = str[3];
                if(s.equals("?")){
                    p.addProperty(people_deathdate, model.createTypedLiteral("None"));
                }else{
                    p.addProperty(people_deathdate, model.createTypedLiteral(s));
                }
            }

            // 添加古代籍贯属性
            str = item[7].split(" ");
            str[1] = str[1].replace("[", " ").replace("]", " ").split(" ")[0];
            s = str[1];
            p.addProperty(people_act_birthplace, model.createTypedLiteral(s));

            // 添加现代籍贯属性
            str = item[8].split(" ");
            str[1] = str[1].replace("[", " ").replace("]", " ").split(" ")[0];
            s = str[1];
            p.addProperty(people_now_birthplace, model.createTypedLiteral(s));

            //添加介绍属性
            str = item[9].split(" ");
            s = str[1];
            p.addProperty(people_intro, model.createTypedLiteral(s));

            //System.out.println();
        }

        // 读取原始event.csv文件
        BufferedReader reader2 = new BufferedReader(new FileReader("./data/datasets/event.csv"));
        String line2;
        while ((line2 = reader2.readLine()) != null) {
            // CSV格式文件为逗号分隔符文件，这里根据逗号切分
            String item[] = line2.split(", ");
            // 对每一个item的内容，将属性名和值提取出来
            for (int i = 0; i < item.length; i++) {
                item[i] = item[i].replace("{", "").replace("\'", "").replace(
                        ":", "").replace("}", "");
            }

            // participants为涉及人物的个数
            int participants = item.length - 7;

            String str[];
            str = item[0].split(" ");
            String name = str[1];
            // 添加一个事件样本
            Individual e = model.createIndividual(NS + name, event);
            for (Iterator<Resource> temp = e.listRDFTypes(true); temp.hasNext(); ) {
                System.out.println(e.getURI() + " is asserted in class " + temp.next());
            }

            // 添加事件名属性
            e.addProperty(event_name, model.createTypedLiteral(name));

            // 添加发生地点属性
            str = item[1].split(" ");
            String s = str[1];
            e.addProperty(event_occur_place, model.createTypedLiteral(s));

            // 添加章节属性
            str = item[2].split(" ");
            s = str[1];
            e.addProperty(event_chapter, model.createTypedLiteral(s));

            // 添加涉及人物属性
            Resource r;
            for(int j=0; j<participants; j++){
                if(j ==0 ){
                    str = item[3+j].split(" ");
                    if(str.length == 1){
                        break;
                    }
                    String var[] = str[1].replace("[", " ").replace("]", " ").split(" ");
                    if(var.length > 1){
                        str[1] = var[0] + "(" + var[1] + ")";
                    }
                    else{
                        str[1] = var[0];
                    }
                    s = str[1];
                    r = model.createResource(NS + s);
                    if(model.containsResource(r)){
                        e.addProperty(event_people, r);
                    }else{
                        Individual new_p = model.createIndividual(NS+s, people);
                        new_p.addProperty(people_name, model.createTypedLiteral(s));
                        e.addProperty(event_people, new_p);
                    }
                }else{
                    str = item[3+j].split(" ");
                    String var[] = str[0].replace("[", " ").replace("]", " ").split(" ");
                    if(var.length > 1){
                        str[0] = var[0] + "(" + var[1] + ")";
                    }
                    else{
                        str[0] = var[0];
                    }
                    s = str[0];
                    r = model.createResource(NS + s);
                    if(model.containsResource(r)){
                        e.addProperty(event_people, r);
                    }else{
                        Individual new_p = model.createIndividual(NS+s, people);
                        new_p.addProperty(people_name, model.createTypedLiteral(s));
                        e.addProperty(event_people, new_p);
                    }
                }
            }

            // 添加简述属性
            str = item[3 + participants].split(" ");
            s = str[1];
            e.addProperty(event_intro, model.createTypedLiteral(s));

            // 添加提示属性
            str = item[4 + participants].split(" ");
            s = str[1];
            e.addProperty(event_hint, model.createTypedLiteral(s));

            // 添加历史属性
            str = item[5 + participants].split(" ");
            s = str[1];
            e.addProperty(event_history, model.createTypedLiteral(s));

            // 添加时间属性
            str = item[6 + participants].split(" ");
            s = str[1];
            e.addProperty(event_date, model.createTypedLiteral(s));

        }

        model.write(new FileOutputStream(new File(Output_file)),"RDF/XML");
    }
}
