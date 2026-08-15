# Contenido extraído de en.subject.pdf

_Páginas: 24_

## Página 1

                                    Fly-in

                       Drones are interesting.











Summary: Designanefficientdroneroutingsystemthatnavigatesmultipledrones
throughconnectedzoneswhileminimizingsimulationturnsandhandlingmovement
                                    constraints.

                                   Version:1.5

## Página 2

Contents


I     Foreword                                                2

II    AIInstructions                                   3

III   CommonInstructions                              5
   III.1   GeneralRules. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    5
   III.2   Makefile. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    5
   III.3   AdditionalGuidelines. . . . . . . . . . . . . . . . . . . . . . . . . . .    6

IV    Introduction                                          7

V    Constraints                                                8

VI    Letthedronefly                                          9

VII   MandatoryPart                                         11
   VII.1  PathfindingandAlgorithmRequirements. . . . . . . . . . . . . . . .   11
   VII.2  ZoneOccupancyRules. . . . . . . . . . . . . . . . . . . . . . . . . .   12
   VII.3  MovementandTurnMechanics. . . . . . . . . . . . . . . . . . . . . .   12
   VII.4  ParserConstraints. . . . . . . . . . . . . . . . . . . . . . . . . . . . .   13
   VII.5  SimulationOutputFormat. . . . . . . . . . . . . . . . . . . . . . . .   15
   VII.6  ScoringSystem. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   15
   VII.7  PerformanceBenchmarks. . . . . . . . . . . . . . . . . . . . . . . . .   17

VIII  ReadmeRequirements                                     20

IX    BonusPart                                              21

X    Submissionandpeer-review                               22


















                                               1

## Página 3

ChapterI

Foreword



DroneshavebeenusedtoherdsheepinNewZealand,replacingsheepdogswithbuzzing
aerialshepherds.InJapan,officebuildingsdeploydronesthatplayloudmusicandflash
lightstoliterallychaseoverworkedemployeeshome. Onedronewastrainedtopaint
graffitionwallsmid-flight—arebelliousblendoftechandstreetart. InSweden,sci-
entistsuseddronestosniffoutwhalepoopfloatingontheoceantostudyendangered
species.Someexperimentaldronesareshapedlikebirdsorinsectstospywithoutbeing
noticed,flappingwingsandall.There’sevenadronethatfliesbyflappingsoapbubbles,
nopropellersinvolved. Involcanoresearch,adroneonceflewstraightintoaneruption
cloud,meltedmid-air,butmanagedtosendbackdatajustsecondsbeforedisintegration.
AndinSouthKorea,synchronizeddroneshowshavereplacedfireworks—safer,silent,
andsomehowevenmoremagical.

Thephrasecomesfromtheideathatthewheelisabrilliantinventionthat’sbeenaround
foreverandworksreallywell. Sincethere’snothingwrongwithit,tryingtoinventit
againwouldn’treallyhelpandcouldbeawasteoftime—especiallywhenthattimecould
bespentsolvingnewproblemsinstead.

Inprogramming,thishappenswhensomeonebuildssomethingfromscratchthatalready
exists—likewritingyourownsortingalgorithmorframeworkwhensolid,open-source
versionsarealreadyoutthere.Butit’snotallbad:doingityourselfcanbeagreatway
tolearnhowthingsworkunderthehood.Thekeyistofindabalance—don’trebuild
everything,buttaketimetoexplorehowthetoolsyou’reusingactuallywork.Thatway,
you’llgrowasadeveloperwithoutgettingstuckreinventingthesameoldwheels.
















                                            2

## Página 4

ChapterII

AIInstructions


●Context

Duringyourlearningjourney,AIcanassistwithmanydifferenttasks.Takethetimeto
explorethevariouscapabilitiesofAItoolsandhowtheycansupportyourwork. How-
ever,alwaysapproachthemwithcautionandcriticallyassesstheresults. Whetherit’s
code,documentation,ideas,ortechnicalexplanations,youcanneverbecompletelysure
thatyourquestionwaswell-formedorthatthegeneratedcontentisaccurate.Yourpeers
areavaluableresourcetohelpyouavoidmistakesandblindspots.


●Mainmessage

  ☛UseAItoreducerepetitiveortedioustasks.

  ☛Developpromptingskills—bothcodingandnon-coding—thatwillbenefityour
     futurecareer.

  ☛LearnhowAIsystemsworktobetteranticipateandavoidcommonrisks,biases,
     andethicalissues.
  ☛Continuebuildingbothtechnicalandpowerskillsbyworkingwithyourpeers.

  ☛OnlyuseAI-generatedcontentthatyoufullyunderstandandcantakeresponsibility
     for.

●Learnerrules:

   •YoushouldtakethetimetoexploreAItoolsandunderstandhowtheywork,so
     youcanusethemethicallyandreducepotentialbiases.

   •Youshouldreflectonyourproblembeforeprompting—thishelpsyouwriteclearer,
     moredetailed,andmorerelevantpromptsusingaccuratevocabulary.

   •Youshoulddevelopthehabitofsystematicallychecking,reviewing,questioning,
     andtestinganythinggeneratedbyAI.

   •Youshouldalwaysseekpeerreview—don’trelysolelyonyourownvalidation.

                                           3

## Página 5

            Fly-in                                                    Dronesareinteresting.

            ●Phaseoutcomes:

                •Developbothgeneral-purposeanddomain-specificpromptingskills.

                •BoostyourproductivitywitheffectiveuseofAItools.

                •Continuestrengtheningcomputationalthinking,problem-solving,adaptability,and
                  collaboration.

            ●Commentsandexamples:

                •You’llregularlyencountersituations—exams,evaluations,andmore—where
                  youmustdemonstraterealunderstanding. Beprepared,keepbuildingbothyour
                  technicalandinterpersonalskills.

                •Explainingyourreasoninganddebatingwithpeersoftenrevealsgapsinyourun-
                  derstanding.Makepeerlearningapriority.

                •AItoolsoftenlackyourspecificcontextandtendtoprovidegenericresponses.Your
                  peers,whoshareyourenvironment,canoffermorerelevantandaccurateinsights.

                •WhereAItendstogeneratethemostlikelyanswer,yourpeerscanprovidealter-
                  nativeperspectivesandvaluablenuance.Relyonthemasaqualitycheckpoint.


                ✓Goodpractice:





                ✗Badpractice:





                ✓Goodpractice:





                ✗Badpractice:










IletCopilotgeneratemycodeforakeypartofmyproject. Itcompiles,butIcan’tIask AIto writea whole function, copy-paste itinto my project. Duringpeer-4
IaskAI:“HowdoItestasortingfunction?”Itgivesmeafewideas.Itrythemoutevaluation,Ican’texplainwhatitdoesorwhy. Ilosecredibility—andIfailmyIuseAItohelpdesignaparser.ThenIwalkthroughthelogicwithapeer.Wecatchexplainhowithandlespipes. Duringtheevaluation,IfailtojustifyandIfailmy
andreviewtheresultswithapeer.Werefinetheapproachtogether.project.twobugsandrewriteittogether—better,cleaner,andfullyunderstood.project.

## Página 6

ChapterIII

CommonInstructions


III.1  GeneralRules

   •YourprojectmustbewritteninPython3.10orlater.

   •Yourprojectmustadheretotheflake8codingstandard.

   •Yourfunctionsshouldhandleexceptionsgracefullytoavoidcrashes.Usetry-except
      blockstomanagepotentialerrors.Prefercontextmanagersforresourceslikefilesor
      connectionstoensureautomaticcleanup.Ifyourprogramcrashesduetounhandled
      exceptionsduringthereview,itwillbeconsiderednon-functional.

   •Allresources(e.g.,filehandles,networkconnections)mustbeproperlymanagedto
      preventleaks.Usecontextmanagerswherepossibleforautomatichandling.

   •Yourcodemustincludetypehintsforfunctionparameters,returntypes,andvari-
      ableswhereapplicable(usingthetypingmodule).Usemypyforstatictypecheck-
      ing.Allfunctionsmustpassmypywithouterrors.

   •Include docstrings in functions and classes following PEP 257 (e.g., Google or
      NumPystyle)todocumentpurpose,parameters,andreturns.

III.2  Makefile

IncludeaMakefileinyourprojecttoautomatecommontasks. Itmustcontainthe
followingrules(mandatorylintimpliesthespecifiedflags;itisstronglyrecommendedto
try–strictforenhancedchecking):

   •install: Installprojectdependenciesusingpip,uv,pipx,oranyotherpackage
      managerofyourchoice.

   •run:Executethemainscriptofyourproject(e.g.,viaPythoninterpreter).

   •debug:RunthemainscriptindebugmodeusingPython’sbuilt-indebugger(e.g.,
      pdb).

   •clean: Removetemporaryfilesorcaches(e.g.,__pycache__,.mypy_cache)to
      keeptheprojectenvironmentclean.


                                              5

## Página 7

Fly-in                                                    Dronesareinteresting.


   •lint:Executethecommandsflake8 .andmypy .--warn-return-any
      --warn-unused-ignores--ignore-missing-imports--disallow-untyped-defs
      --check-untyped-defs

   •lint-strict(optional):Executethecommandsflake8 .andmypy . --strict

III.3  AdditionalGuidelines

   •Createtestprogramstoverifyprojectfunctionality(notsubmittedorgraded).Use
      frameworkslikepytestorunittestforunittests,coveringedgecases.

   •Includea.gitignorefiletoexcludePythonartifacts.

   •Itisrecommendedtousevirtualenvironments(e.g.,venvorconda)fordependency
      isolationduringdevelopment.


Ifanyadditionalproject-specificrequirementsapply,theywillbestatedimmediatelybelow
thissection.





































                                              6

## Página 8

ChapterIV

Introduction



Autonomousdronesarethefutureoftransportation. Theyarealreadyusedinmany
industries,suchasagriculture,construction,andlogistics.Theyarealsousedinmilitary
operations,suchassurveillanceandreconnaissance.

Yourtaskistodesignasystemthatefficientlyroutesafleetofdronesfromacentral
base(start)toatargetlocation(end),whilenavigatingthisdynamicnetworkunder
asetofstrictconstraintsandoptimizationgoals.

You’llbegivenagraphrepresentingthenetworkofzones,andasetofconstraints
thatyoumustrespect.

Thegraphisrepresentedasanetworkofconnectedzones,whereconnectionsdefinepos-
siblemovementpathsbetweenzones.




























                                            7

## Página 9

ChapterV

Constraints



   •Anylibrarythathelpswithgraphlogicisforbidden(suchasnetworkx,graphlib,
     etc.).

   •Theprojectmustbecompletelytypesafe.Usingflake8andmypyismandatory.

   •Theprojectmustbecompletelyobject-oriented.

Thiswillhavetobedemonstratedduringthepeerreview.



































                                           8

## Página 10

ChapterVI

Letthedronefly



Attachedtothissubject,you’llfindmultiplefilesthatrepresentthenetworkofzonesin
thefollowingformat:
Example:

 nb_drones:  5

 start_hub:  hub  0  0  [color=green]
 end_hub:  goal  10  10  [color=yellow]
 hub:  roof1  3  4  [zone=restricted  color=red]
 hub:  roof2  6  2  [zone=normal  color=blue]
 hub:  corridorA  4  3  [zone=priority  color=green  max_drones=2]
 hub:  tunnelB  7  4  [zone=normal  color=red]
 hub:  obstacleX  5  5  [zone=blocked  color=gray]
 connection:  hub-roof1
 connection:  hub-corridorA
 connection:  roof1-roof2
 connection:  roof2-goal
 connection:  corridorA-tunnelB  [max_link_capacity=2]
 connection:  tunnelB-goal
Interesting,right?Tobemoreprecise:

    •Thefirstlinedefinesthenumberofdronesusingnb_drones:  <number>.

    •Zonedefinitiononeachlineusingtypeprefixes:

          ◦start_hub:  <name> <x> <y> [metadata]marksthestartingzone.
          ◦end_hub:  <name> <x> <y> [metadata]markstheendzone.
          ◦hub:  <name> <x> <y> [metadata]definesaregularzone.
          ◦Theconnectionsyntaxforbidsdashesinzonenames(seebelow).

    •Allmetadataisoptionalandenclosedinbrackets[...]withdefaultvalues:

          ◦zone=<type>(default:normal)
          ◦color=<value>(default:none)
          ◦max_drones=<number>(default: 1)-Maximumdronesthatcanoccupythis
             zonesimultaneously
          ◦Tagsinsidebracketscanappearinanyorder.

    •Zonetypes:


                                                     9

## Página 11

Fly-in                                                    Dronesareinteresting.


         ◦normal–Standardzonewith1turnmovementcost(default)
         ◦blocked–Inaccessiblezone.Dronesmustnotenterorpassthroughthiszone.
            Anypathusingitisinvalid.
         ◦restricted–Asensitiveordangerouszone. Movementtothiszonecosts2
            turns.
         ◦priority–Apreferredzone.Movementtothiszonecosts1turnbutshould
            beprioritizedinpathfinding.

   •Colors:

         ◦Colorsareoptionalandcanbeusedforvisualrepresentation(terminaloutput
            orgraphicaldisplay).
         ◦Acceptedvaluesforcolorareanyvalidsingle-wordstrings(e.g.,red,blue,
            gray).Thereisnofixedlistofallowedcolors.
         ◦Whencolorsarespecified,theimplementationshouldprovidevisualfeedback
            throughcoloredterminaloutputorgraphicalrepresentation.

   •Connectionsaredefinedusingconnection:  <name1>-<name2> [metadata]:

         ◦Defineabidirectionalconnection(edge)betweentwozones.
         ◦Theconnectionsyntaxforbidsdashesinzonenames.
         ◦Optionalmetadatacanbespecifiedinbrackets[...]:
              ∗max_link_capacity=<number>(default: 1)-Maximumdronesthatcan
                traversethisconnectionsimultaneously

   •Commentsstartwith’#’andareignored.




               The  zones  coordinates  will  always  be  integers,  and  there  will  always
               be  a  unique  start  and  a  unique  end  zone.




















                                                10

## Página 12

ChapterVII

MandatoryPart



Asyoumayhaveguessed,themainobjectiveistomovealldronesfromthestartzone
totheendzoneinthefewestpossiblesimulationturns.


VII.1  PathfindingandAlgorithmRequirements

   •Dronesmaymovesimultaneously.Thealgorithmmustschedulepathstomaximize
     throughputandavoidunnecessarydelays.

   •Yourimplementationmusthandle:

        ◦Distributionofdronesacrossmultiplepaths.
        ◦Strategicwaitingwhenmovementisnotpossible.
        ◦Avoidanceofpathconflictsanddeadlocks.

   •Thealgorithmmusttakeintoaccount:

        ◦Pathlengths,includingmovementcostsassociatedwithzonetypes(e.g.,re-
          strictedorpriority).
        ◦Turnscheduling,topreventdronesfromcollidingorblockingeachother.
        ◦Graphstructure,todetermineavailabledisjointoroverlappingpaths.
        ◦Zonecapacityconstraints(max_drones)andconnectioncapacity(max_link_capacity).

   •Youralgorithmshouldbeadaptable: differentmapsmayrequiredifferentrouting
     strategies,dependingonthetopologyandzonetypes.

   •VisualRepresentation: Yourimplementationmustprovidevisualfeedbackof
     thesimulation,eitherthrough:

        ◦Coloredterminaloutputshowingdronemovementsandzonestates
        ◦Agraphicalinterfacedisplayingthenetworkanddronepositions
        ◦Bothoptionsforenhanceduserexperience



                                           11

## Página 13

Fly-in                                                    Dronesareinteresting.



                   •How  efficient  is  your  algorithm?
                   •Can  it  work  with  a  large  number  of  drones?

                   •What  is  the  complexity  (e.g.,  O(n),  O(log  n),  etc.)?

                   •Are  you  recalculating  or  caching  paths?

                   •How  does  it  impact  memory  usage?

                   •How  does  your  visual  representation  enhance  understanding  of
                     the  simulation?

VII.2  ZoneOccupancyRules

   •Bydefault,azonemaycontainatmostonedroneatanygivensimulationturn.

   •Zoneswithmax_drones=NmetadatacancontainuptoNdronessimultaneously.

   •Theonlyspecialexceptionstooccupancyrulesare:

         ◦Thestartzone:alldronesbeginhereandmaysharethespaceinitially.
         ◦Theendzone:multipledronescanarrivehereandareconsidereddelivered.

   •Twodronesmaynotenterthesamezoneonthesameturnunlessthezone’scapacity
      allowsit.

   •Adronemaynotmoveintoazonethatwouldexceeditsmaximumcapacity.

   •Connectioncapacity(max_link_capacity)definedonconnectionslimitshowmany
      dronescantraversethesameconnectionsimultaneously.

   •Dronesmaymovesimultaneously,aslongasallcapacityconstraintsarerespected.

VII.3  MovementandTurnMechanics

Thesimulationproceedsindiscreteturns.Ateachturn,everydronemay:

   •Movetoanadjacentconnectedzone(ifcapacityallows).

   •Movetoaconnectiontowardsarestrictedzone(thatrequires2turnstobereached).
      Inthiscase,thedroneMUSTreachitsdestinationduringthenextturn. Itcan’t
      waitextraturnsontheconnection.

   •Stayinplace(e.g.,towait,orifmovementisblocked).

Thesimulationmustpreventconflictsandensurevalidmovementschedulingbasedon
turn-by-turnstateevaluation:

   •Dronesmovingoutofazonefreeupcapacityforthatsameturn.

   •Azonemusthaveavailablecapacityforadronetomoveintoit(afteralldrones
      movingouthavefreedupspace).

                                              12

## Página 14

Fly-in                                                    Dronesareinteresting.


   •Formulti-turnmovements(restrictedzones),thedroneoccupiestheconnection
      duringtransitandMUSTarriveatthedestinationafterthespecifiednumberof
      turns.Itcannotwaitontheconnectionforanemptyspaceinthedestinationzone.

Eachmovementbetweenzoneshasacostinturns, basedonthezone=typeofthe
destination:

   •normal:1turn(default)

   •restricted:2turns

   •priority:1turn(butshouldbepreferredinpathfindingalgorithms)

   •blocked:Inaccessible—cannotbeentered

VII.4  ParserConstraints

Theinputfilemustrespecttheexpectedstructureandsyntax:

   •Thefirstlinemustdefinethenumberofdronesusingnb_drones:  <positive_integer>.

   •Theprogrammustbeabletohandleanynumberofdrones.

   •Theremustbeexactlyonestart_hub:zoneandoneend_hub:zone.

   •Eachzonemusthaveauniquenameandvalidintegercoordinates.

   •Zonenamescanuseanyvalidcharactersexceptdashesandspaces.

   •Connectionsmustlinkonlypreviouslydefinedzonesusingconnection:  <zone1>-<zone2>
      [metadata].

   •Thesameconnectionmustnotappearmorethanonce(e.g.,a-bandb-aarecon-
      sideredduplicates).

   •Anymetadatablock(e.g.,[zone=...  color=...]forzones,[max_link_capacity=...]
      forconnections)mustbesyntacticallyvalid.

   •Zonetypesmustbeoneof:normal,blocked,restricted,priority.Anyinvalid
      typemustraiseaparsingerror.

   •Capacityvalues(max_dronesforzones,max_link_capacityforconnections)must
      bepositiveintegers.

   •Themax_dronescapacityisignoredonthestart_hubandend_hubzones: these
      havenocapacitylimit(alldronesmaystartinthestartzone,andanynumberof
      dronesmaybedeliveredtotheendzone).Ifsuchmetadataispresentonthosetwo
      zones,itisignoredandisnotavalidationerror.

   •Anyotherparsingerrormuststoptheprogramandreturnaclearerrormessage
      indicatingthelineandcause.



                                             13

## Página 15

Fly-in                                                    Dronesareinteresting.




                  It’s  highly  recommended  to  make  your  own  map  files  on  top  of  the  ones
                  provided  in  the  subject  for  handling  edge  cases  and  error  handling.
























































                                                        14

## Página 16

Fly-in                                                    Dronesareinteresting.

VII.5  SimulationOutputFormat

   •Thesimulationmustoutputthestep-by-stepmovementofdronesfromthestartto
      theendzone.

   •Eachsimulationturnisrepresentedbyaline.

   •A line must list all the drone movements that occur during that turn, space-
      separated.Eachmovementmustfollowtheformat:D<ID>-<zone>,orD<ID>-<connection>
      incaseofdronesstillinflighttowardrestrictedzones.

        ◦D<ID>referstotheuniquedroneidentifier(e.g.,D1,D2).
        ◦<zone>isthenameofthedestinationzone.
        ◦<connection>isthenameoftheconnectiontowardarestrictedzone.

   •Dronesthatdonotmoveinagiventurnareomittedfromthatline.

   •Dronesthatreachtheendzoneareconsidereddeliveredandarenolongertracked.

   •Thesimulationendswhenalldroneshavereachedtheendzone.

   •Example:

           D1-roof1 D2-corridorA
           D1-roof2 D2-tunnelB
           D1-goal D2-goal


VII.6  ScoringSystem

   •Theperformanceofasolutionisevaluatedbasedonthetotalnumberofsimu-
      lationturnsrequiredtoroutealldronesfromthestartzonetotheendzone.

   •Thefewerthenumberofturns,thebetterthescore.

   •Avalidsimulationmust:

        ◦Complywithallmovementandoccupancyrules.
        ◦Correctlyhandlemovementcostsassociatedwithzonetypes.
        ◦Respectallcapacityconstraints(zoneandconnectionlimits).
        ◦Avoidallconflicts(e.g.,exceedingzoneorconnectioncapacity).

Secondary(optional)evaluationmetricsmayinclude:

   •Thenumberofdronesmovedperturn(efficiencyofpathallocation).

   •Theaveragenumberofturnsperdrone.

   •Thetotalpathcost(sumofweightedmovementcostsacrossalldrones).

                                             15

## Página 17

Fly-in                                                    Dronesareinteresting.


    •Qualityandusefulnessofvisualrepresentation.

Incaseofidenticalturncounts,solutionsmaybecomparedbasedonsecondarymetrics
orcodequality.


                 These  secondary  metrics  are  not  mandatory  to  compute  automatically,
                 but  learners  are  encouraged  to  display  them  in  their  simulation
                 output  or  documentation  to  help  peers  evaluate  performance.


















































                                                    16

## Página 18

Fly-in                                                    Dronesareinteresting.

VII.7  PerformanceBenchmarks

Thefollowingperformancetargetsdefinetheexpectedoptimizationlevelyourimplemen-
tationmustachieve.
   •Expectedperformance:

         ◦Easymapsshouldbesolvedinlessthan10turns
         ◦Mediummapsshouldbesolvedin10–30turns
         ◦Hardmapsshouldbesolvedinlessthan60turns
         ◦Challengermap(optional)shouldaimtobeatthereferencerecordof45turns
           Thislevelispurelyoptionalanddoesnotaffectyourgrade.
Tohelpyouevaluateyouralgorithm’sefficiency,herearereferenceperformancetargets
basedontheprovidedtestmaps:

   •EasyMaps:
         ◦Linearpathwith2drones:Target≤6turns
         ◦Simpleforkwith4drones:Target≤8turns
         ◦Basiccapacitywith4drones:Target≤6turns

   •MediumMaps:

         ◦Deadendtrapwith5drones:Target≤12turns
         ◦Circularloopwith6drones:Target≤15turns
         ◦Prioritypuzzlewith5drones:Target≤12turns
   •HardMaps:

         ◦Mazenightmarewith8drones:Target≤30turns
         ◦Capacityhellwith12drones:Target≤35turns
         ◦Ultimatechallengewith15drones:Target≤45turns
   •ChallengerMap(optional—forexceptionalimplementations):

         ◦TheImpossibleDreamwith25drones:Referencerecord:45turns
         ◦Thisquasi-unsolvablechallengeisdesignedforalgorithmicresearchandopti-
           mization
         ◦Solvingthismapdemonstratesexceptionalpathfindingandoptimizationskills
         ◦Note:Thislevelispurelyoptionalanddoesnotaffectyourgrade



               These  benchmarks  are  provided  as  optimization  targets  to  help  you
               evaluate  your  algorithm’s  performance.    Meeting  these  targets
               demonstrates  a  well-optimized  implementation  and  will  be  assessed
               during  peer  evaluation.

                                              17

## Página 19

Fly-in                                                    Dronesareinteresting.



                       •Can  your  algorithm  meet  these  performance  benchmarks?
                       •How  does  your  solution  compare  to  the  reference  targets?

                       •What  optimizations  did  you  implement  to  achieve  better
                         performance?

                       •Can  you  solve  the  Challenger  map  and  beat  the  45-turn  record?























                                          FigureVII.1:Map easy 2
























                                       FigureVII.2:Map medium 3


                                                        18

## Página 20

Fly-in                                                    Dronesareinteresting.



















                                     FigureVII.3:Map hard 2









































                                                 19

## Página 21

ChapterVIII

ReadmeRequirements



AREADME.mdfilemustbeprovidedattherootofyourGitrepository. Itspurposeis
toallowanyoneunfamiliarwiththeproject(peers, staff, recruiters, etc.) toquickly
understandwhattheprojectisabout,howtorunit,andwheretofindmoreinformation
onthetopic.
TheREADME.mdmustincludeatleast:
   •Theveryfirstlinemustbeitalicizedandread:Thisprojecthasbeencreatedaspart
      ofthe42curriculumby<login1>[,<login2>[,<login3>[...]]].
   •A“Description”sectionthatclearlypresentstheproject,includingitsgoalanda
      briefoverview.

   •An“Instructions”sectioncontaininganyrelevantinformationaboutcompilation,
      installation,and/orexecution.

   •A“Resources”sectionlistingclassicreferencesrelatedtothetopic(documen-
      tation,articles,tutorials,etc.),aswellasadescriptionofhowAIwasused—
      specifyingforwhichtasksandwhichpartsoftheproject.

  ➠Additionalsectionsmayberequireddependingontheproject(e.g.,usage
      examples,featurelist,technicalchoices,etc.).



Anyrequiredadditionswillbeexplicitlylistedbelow.


   •Adetaileddescriptionofyouralgorithmchoicesandimplementationstrategymust
      alsobeincluded.
   •Documentationofthevisualrepresentationfeaturesandhowtheyenhancetheuser
      experience.




              Your  README  must  be  written  in  English.




                                             20

## Página 22

ChapterIX

BonusPart



ThisBonuspartwillbereviewedonlyifallthemandatoryrequirementsaremet.

Herearefeaturesyoucanimplementtoenhanceyourproject:

   •Exceptionalperformance:

        ◦You’perfectly’meettheperformancereferencetargetsforallprovidedmaps.
        ◦’perfectly’meansyoumatchorbeatthetargetturncount.

   •Challengermap:

        ◦TheImpossibleDreammapissolvedandbeatsthereferencerecordof45
          turns.





























                                         21

## Página 23

ChapterX

Submissionandpeer-review



SubmityourassignmentinyourGitrepositoryasusual. Onlytheworkinsideyour
repositorywillbeevaluatedduringthepeer-evaluation. Don’thesitatetodouble-check
thenamesofyourfilestoensuretheyarecorrect.






               Place  all  your  files  at  the  root  of  your  repository.



AfullyworkingsimulationwritteninPython,including:
   •Aparserfortheinputfileformat.

   •Asimulationenginerespectingmovementandzonerules.

   •Apathfindingalgorithm(ormultiple)capableofminimizingtotalturns.

   •Avisualrepresentationsystem(terminalcolorsand/orgraphicalinterface).

   •Aterminalorlogoutputthatfollowsthespecifiedformat.




               Note  that  we  may  ask  you  to  explain  your  code  or  possibly  even  to
               write  some  code.    Make  sure  to  be  prepared  for  this.






               Evaluation  maps  may  be  different  from  the  ones  provided  in  the
               subject.



Duringtheevaluation,abriefmodificationoftheprojectmayoccasionallybere-
quested. Thiscouldinvolveaminorbehaviourchange,afewlinesofcodetowriteor

                                               22

## Página 24

Fly-in                                                    Dronesareinteresting.


rewrite,oraneasy-to-addfeature.

Whilethisstepmaynotbeapplicabletoeveryproject,youmustbepreparedforit
ifitismentionedintheevaluationguidelines.

Thisstepismeanttoverifyyouractualunderstandingofaspecificpartoftheproject.
Themodificationcanbeperformedinanydevelopmentenvironmentyouchoose(e.g.,
yourusualsetup),anditshouldbefeasiblewithinafewminutes—unlessaspecifictime
frameisdefinedaspartoftheevaluation.
Youcan,forexample,beaskedtomakeasmallupdatetoafunctionorscript,modifya
display,oradjustadatastructuretostorenewinformation,etc.

Thedetails(scope,target,etc.)willbespecifiedintheevaluationguidelinesandmay
varyfromoneevaluationtoanotherforthesameproject.











































                                             23
